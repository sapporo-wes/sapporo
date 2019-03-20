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

Using docker-compose.

```shell
$ git clone https://github.com/suecharo/SAPPORO.git
$ cd SAPPORO/SAPPORO-web
$ docker-compose up -d
```

Access `localhost:1121/` using the browser.

![SAPPORO - Home](https://i.imgur.com/ebHAY8o.jpg)

## Usage

### Managing User

There are two types of user: the general user and the administrator user. The difference is whether it can access the administration page.

---

The administrator user creates it as follows.

```shell
$ docker-compose exec app python3 /opt/SAPPORO-web/SAPPORO-web/manage.py createsuperuser
```

---

The general users creates using Sign Up.

![SAPPORO - Signup](https://i.imgur.com/fsAoJc9.jpg)

If you want to disable Sign Up, edit `./docker-compose.yml`.

```shell
    environment:
      - ENABLE_USER_SIGNUP=True  # True or False
```

---

User management uses Django Native. Please access to `localhost:1121/django-admin` as an administrator user.

### Add SAPPORO-service

After logging in as an administrator user, select [Admin] - [Managing services] in the header.

![SAPPORO - Managing Service](https://i.imgur.com/IaEqRo1.png)

You can add SAPPORO-service by entering service information in the form.

---

For your information, if you use the same docker host between SAPPORO-web and SAPPORO-service, you can check the IP adress of docker host by the following way.

```shell
$ docker-compose exec app ip route
default via 192.168.224.1 dev eth0    # THIS!!
192.168.224.0/20 dev eth0 scope link  src 192.168.224.3
```

## Running Workflow

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

As an initial setting, Nginx provides `localhost:1121` as a Web endpoint. If you want to change the port, change the following part of `./docker-compose.yml`.

```yaml
ports:
  - 1121:80 # HERE
```

---

If you want to use SSL/TSL, edit `./config/nginx.conf`.

### Logging

The following items are output as logs.

```shell
$ ls ./log
django.log  nginx-access.log  nginx-error.log  nginx.pid  uwsgi.log  uwsgi.pid
```

---

Logs are normally outputed to `./log`. If you want to change the output location, edit `./docker-compose.yml`.

```shell
--- docker-compose.yml	2019-03-06 10:37:53.403787949 +0900
+++ docker-compose.log.yml	2019-03-06 10:38:35.055851639 +0900
@@ -12,7 +12,7 @@
     volumes:
       - ./SAPPORO-web:/opt/SAPPORO-web/SAPPORO-web
       - ./config:/opt/SAPPORO-web/config
-      - ./log:/opt/SAPPORO-web/log
+      - /var/log/SAPPORO-web:/opt/SAPPORO-web/log
     environment:
       - LOG_LEVEL=INFO # DEBUG or INFO
       - LANGUAGE_CODE=en
```

---

To change the log level, edit `./docker-compose.yml`. When set as `LOG_LEVEL=DEBUG`, detailed logs and traceback of Python are displayed in `./log/flask.log`.

```shell
    environment:
      - LOG_LEVEL=INFO # DEBUG or INFO
```

---

If you want log rotation of `./log/django.log`, edit `./SAPPORO-web/config/logging_config.py`.

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

You can develop using Django's lcoal server. As a result, code changes are reflected immediately on the server. Files containing dev as the name in `./test` are used as the configuration files.

```shell
$ cd test
$ docker-compose -f docker-compose.dev.yml up -d --build
$ docker-compose -f docker-compose.dev.yml exec app /bin/bash /opt/SAPPORO-web/test/migrate.sh
$ docker-compose -f docker-compose.dev.yml exec app python3 /opt/SAPPORO-web/SAPPORO-web/manage.py createsuperuser
$ docker-compose -f docker-compose.dev.yml exec app /bin/bash /opt/SAPPORO-web/test/run_server.sh
```
