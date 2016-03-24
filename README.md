CronBeat: error reporting to [OpBeat](https://opbeat.com/) of commands run via cron
================================================

CronBeat is a python command-line wrapper that reports errors to [OpBeat](http://opbeat.com) (using [opbeat](https://github.com/opbeat/opbeat_python)) if the called script exits with a status other than zero.

Install
-------

`pip install https://github.com/linuxlefty/CronBeat/archive/master.zip`

Usage
-----

```
usage: runner.py [-h] [-O ORG_ID] [-A APP_ID] [-t SECRET_TOKEN]
                 [-M STRING_MAX_LENGTH] [-q] [--version]
                 ...

Wraps commands and reports those that fail to OpBeat.

positional arguments:
  cmd                   The command to run

optional arguments:
  -h, --help            show this help message and exit
  -O ORG_ID, --organization ORG_ID
                        OpBeat organization ID (can also be set via the
                        OPBEAT_ORGANIZATION_ID environment variable
  -A APP_ID, --app APP_ID
                        OpBeat application ID (can also be set via the
                        OPBEAT_APP_ID environment variable
  -t SECRET_TOKEN, --token SECRET_TOKEN
                        OpBeat secret token (can also be set via the
                        OPBEAT_SECRET_TOKEN environment variable
  -M STRING_MAX_LENGTH, --string-max-length STRING_MAX_LENGTH, --max-message-length STRING_MAX_LENGTH
                        The maximum characters of a string that should be sent
                        to OpBeat (defaults to 400)
  -q, --quiet           suppress all command output
  --version             show program's version number and exit
```

Example
-------

`crontab -e`
```
OPBEAT_ORGANIZATION_ID=<your_org_id>
OPBEAT_APP_ID=<your_app_id>
OPBEAT_SECRET_TOKEN=<your_secret_token>

0 4 * * * cronbeat my-process --arg arg2
```


License
-------

This project is based off of the excellent [cron-sentry](https://github.com/Yipit/cron-sentry) by Yipit Inc.

Original copyright 2015 to Yipit Inc. (MIT license).

Copyright 2016 to Peter Naudus. (MIT license).
