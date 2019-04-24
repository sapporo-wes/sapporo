# SAPPORO-web

SAPPORO-service is a Web front-end for managing users and batch jobs.

[Japanese Document](https://hackmd.io/s/r1_mSHn8V)

## Environment

The development and verification environments are as follows.

```shell
$ docker --version
Docker version 18.09.1, build 4c52b90
$ docker-compose --version
docker-compose version 1.23.1, build b02f1306
```

We are checking with Ubuntu 16.04 and macOS Mojave.

```shell
$ cat /etc/os-release
NAME="Ubuntu"
VERSION="16.04.5 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.5 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial

$ sw_vers
ProductName:    Mac OS X
ProductVersion: 10.14.3
BuildVersion:   18D109
```

Python libraries being used are described in [requirements.txt](https://github.com/suecharo/SAPPORO/blob/master/SAPPORO-service/requirements.txt).

## Easy Deployment

Use a script that wraps docker-compose.

```shell
$ git clone https://github.com/suecharo/SAPPORO.git
$ cd SAPPORO/SAPPORO-web/script
$ ./web-up --help
Usage: web-up [Option]...
Script to up SAPPORO-web.

Option:
  -h, --help                  Print usage.
  -l, --log-level INFO|DEBUG  Set log level. (default INFO)
  -p, --port PORT             Set the host TCP/IP port. (default 1121)
  -t, --timezone TIMEZONE     Set the timezone. (default Asia/Tokyo)
  --log-dir ABS_PATH          Set log dir. (default SAPPORO-web/log)
  --user-signup TRUE|FALSE    Enable user signup. (default True)

$ ./web-up
# Access `localhost:1121/` using the browser.
```

![SAPPORO - Home](https://i.imgur.com/ebHAY8o.jpg)

## Usage

### Manage User

There are two types of user: the general user and the administrator user. The difference is whether it can access the administration page.

---

The administrator user creates it as follows.

```shell
$ ./create_super_user
```

---

The general users create using Sign Up.

![SAPPORO - Signup](https://i.imgur.com/fsAoJc9.jpg)

If you want to disable Sign Up, start SAPPORO-web like `./web-up --user-signup FALSE`.

---

To manage users, after logging in as an admin user, select [Admin] - [Managing users] in the header.

### Add SAPPORO-service

After logging in as an administrator user, select [Admin] - [Managing services] in the header.

![SAPPORO - Managing Service](https://i.imgur.com/IaEqRo1.png)

You can add SAPPORO-service by entering service information in the form.

---

If you are using SAPPORO-service on the same machine, `Service Server Host` is `sapporo-service-web`.

## Run Workflow

Select [Workflow] - [Workflow Name to be executed] in the header.

![SAPPORO - Workflow](https://i.imgur.com/qKk1oxz.png)

When you select [Prepare Run], the form will be displayed, so please enter the execution parameters.

![SAPPORO - Prepare Workflow](https://i.imgur.com/MXW3cn3.png)

When you select [Run Workflow], the batch job starts.

![SAPPORO - Run](https://i.imgur.com/qlvyMbt.png)

### Network

SAPPORO-service is using Django. The network configuration is as follows.

```text
Django <-> uwsgi <-(uWSGI protocol)-> Nginx <-(HTTP)-> Docker <-> User
```

---

As an initial setting, Nginx provides `localhost:1121` as a Web endpoint. If you want to change the port, start SAPPORO-web like `./web-up --port ${PORT_NUM}`.

---

If you want to use SSL/TSL, edit `./config/nginx.conf`.

### Logging

The following items are output as logs.

```shell
$ ls ./log
django.log  nginx-access.log  nginx-error.log  nginx.pid  uwsgi.log  uwsgi.pid
```

---

Logs are normally outputted to `./log`. If you want to change the output location, start SAPPORO-web like `./web-up --log-dir $ {LOG_DIR}`.

---

To change the log level, start SAPPORO-web like `./web-up --log-level DEBUG`. When set as `DEBUG`, detailed logs and traceback of Python are displayed in `./log/flask.log`.

---

If you want log rotation of `./log/django.log`, edit `./SAPPORO-web/config/logging_config.py`.

## Stop and Uninstall

```shell
# Stop
$ ./web-down
# Uninstall
$ ./web-clean
```

## Testing environment

### Execution Test

The Test is done using pytest and coverage.

```shell
$ cd test
$ docker-compose -f docker-compose.dev.yml up -d --build
$ docker-compose -f docker-compose.dev.yml exec app /bin/bash /opt/SAPPORO-web/test/run_test.sh
```

The result is output to `./test/coverage_html`.

### Development environment

You can develop using Django's local server. As a result, code changes are reflected immediately on the server. Files containing dev as the name in `./test` are used as the configuration files.

```shell
$ cd test
$ docker-compose -f docker-compose.dev.yml up -d --build
$ docker-compose -f docker-compose.dev.yml exec app /bin/bash /opt/SAPPORO-web/test/migrate.sh
$ docker-compose -f docker-compose.dev.yml exec app python3 /opt/SAPPORO-web/SAPPORO-web/manage.py createsuperuser
$ docker-compose -f docker-compose.dev.yml exec app /bin/bash /opt/SAPPORO-web/test/run_server.sh
```
