import sys
import opbeat.conf.defaults
from os import getenv, SEEK_END
from opbeat import Client
from opbeat.transport import HTTPTransport
from subprocess import call, list2cmdline
from tempfile import TemporaryFile
from argparse import ArgumentParser, REMAINDER
from sys import argv
from time import time
from .version import VERSION

DEFAULT_STRING_MAX_LENGTH = opbeat.conf.defaults.MAX_LENGTH_STRING

parser = ArgumentParser(description='Wraps commands and reports those that fail to OpBeat.')
parser.add_argument(
    '-O', '--organization',
    metavar='ORG_ID',
    default=getenv('OPBEAT_ORGANIZATION_ID'),
    help='OpBeat organization ID (can also be set via the OPBEAT_ORGANIZATION_ID environment variable',
)
parser.add_argument(
    '-A', '--app',
    metavar='APP_ID',
    default=getenv('OPBEAT_APP_ID'),
    help='OpBeat application ID (can also be set via the OPBEAT_APP_ID environment variable',
)
parser.add_argument(
    '-t', '--token',
    metavar='SECRET_TOKEN',
    default=getenv('OPBEAT_SECRET_TOKEN'),
    help='OpBeat secret token (can also be set via the OPBEAT_SECRET_TOKEN environment variable',
)
parser.add_argument(
    '-M', '--string-max-length', '--max-message-length',
    type=int,
    default=DEFAULT_STRING_MAX_LENGTH,
    help=(
        'The maximum characters of a string that should be sent to OpBeat ' +
        '(defaults to {0})'
    ).format(DEFAULT_STRING_MAX_LENGTH),
)
parser.add_argument(
    '-q', '--quiet',
    action='store_true',
    default=False,
    help='suppress all command output'
)
parser.add_argument(
    '--version',
    action='version',
    version=VERSION,
)
parser.add_argument(
    'cmd',
    nargs=REMAINDER,
    help='The command to run',
)


def run(args=argv[1:]):
    opts = parser.parse_args(args)

    if opts.cmd:
        # make cron-sentry work with both approaches:
        #
        #     cronbeat -- command --arg1 value1
        #     cronbeat command --arg1 value1
        #
        # see more details at https://github.com/Yipit/cron-sentry/pull/6
        if opts.cmd[0] == '--':
            cmd = opts.cmd[1:]
        else:
            cmd = opts.cmd
        runner = CommandReporter(
            cmd=cmd,
            org=opts.organization,
            app=opts.app,
            token=opts.token,
            string_max_length=opts.string_max_length,
            quiet=opts.quiet
        )
        sys.exit(runner.run())
    else:
        sys.stderr.write("ERROR: Missing command parameter!\n")
        parser.print_usage()
        sys.exit(1)


class CommandReporter(object):
    def __init__(self, cmd, org, app, token, string_max_length, quiet=False):
        self.opbeat_org = org
        self.opbeat_app = app
        self.opbeat_token = token
        self.command = cmd
        self.string_max_length = string_max_length
        self.quiet = quiet

    def run(self):
        start = time()

        with TemporaryFile() as stdout:
            with TemporaryFile() as stderr:
                exit_status = call(self.command, stdout=stdout, stderr=stderr)

                last_lines_stdout = self._get_last_lines(stdout)
                last_lines_stderr = self._get_last_lines(stderr)

                if exit_status > 0:
                    elapsed = int((time() - start) * 1000)
                    self.report_fail(exit_status, last_lines_stdout, last_lines_stderr, elapsed)

                if not self.quiet:
                    sys.stdout.write(last_lines_stdout)
                    sys.stderr.write(last_lines_stderr)

                return exit_status

    def report_fail(self, exit_status, last_lines_stdout, last_lines_stderr, elapsed):
        message = "Command failed: \"%s\"" % (list2cmdline(self.command),)

        client = Client(
            transport=HTTPTransport,
            organization_id=self.opbeat_org,
            app_id=self.opbeat_app,
            secret_token=self.opbeat_token,
            string_max_length=self.string_max_length
        )

        client.captureMessage(
            message,
            data={
                'logger': 'cron',
            },
            extra={
                'culprit': list2cmdline(self.command),
                'exit_status': exit_status,
                'last_lines_stdout': last_lines_stdout,
                'last_lines_stderr': last_lines_stderr,
            },
            time_spent=elapsed
        )

    def _get_last_lines(self, buf):
        buf.seek(0, SEEK_END)
        file_size = buf.tell()
        if file_size < self.string_max_length:
            buf.seek(0)
            last_lines = buf.read().decode('utf-8')
        else:
            buf.seek(-(self.string_max_length - 3), SEEK_END)
            last_lines = '...' + buf.read().decode('utf-8')
        return last_lines

if __name__ == "__main__":
    run()
