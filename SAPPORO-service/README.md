# SAPPORO-service

SAPPORO-service is a REST API Server that executes batch jobs. The REST API definition conforms to [GA4GH Workflow Execution Service API](https://github.com/ga4gh/workflow-execution-service-schemas).

[Japanese Document](https://hackmd.io/s/Skp49g2IN)

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
$ cd SAPPORO/SAPPORO-service
$ docker-compose up -d
$ curl -X GET localhost:1122/service-info
{
  "auth_instructions_url": "https://dummy_auth_instructions_url/",
  "contact_info_url": "https://dummy_contact_info_url/",
  "supported_wes_versions": [
    "v1.0.0"
  ],
  "workflow_engines": [
    {
      "engine_name": "cwltool",
      "engine_version": "1.0.20181201184214",
      "workflow_types": [
        {
          "language_type": "CWL",
          "language_version": "v1.0"
        }
      ]
    }
  ]
}
```

### macOS

Need to edit `./docker-compose.yml`.

```shell
--- docker-compose.yml  2019-03-05 22:51:04.612902487 +0900
+++ docker-compose.mac.yml  2019-03-05 23:16:30.253558038 +0900
@@ -9,7 +9,7 @@
     restart: always
     volumes:
       - /var/run/docker.sock:/var/run/docker.sock
-      - /usr/bin/docker:/usr/bin/docker
+      - /usr/local/bin/docker:/usr/bin/docker
       - /tmp:/tmp
       - ./SAPPORO-service:/opt/SAPPORO-service/SAPPORO-service
       - ./config:/opt/SAPPORO-service/config
```

## Usage

### REST API Definition

It is described in Swagger format in `./api-definition/SAPPORO-service-api-definition.yml`. Please confirm by the following method.

- [SAPPORO - Swagger UI](https://suecharo.github.io/SAPPORO/SAPPORO-service/api-definition/swagger-ui)
- [Swagger Editor](https://editor.swagger.io)
- [VSCode - Swagger Viewer](https://marketplace.visualstudio.com/items?itemName=Arjun.swagger-viewer)

### GET /service-info

`GET /service-info` is a REST API method for users to get the details of the service.

```shell
$ curl -X GET localhost:1122/service-info
{
  "auth_instructions_url": "https://dummy_auth_instructions_url/",
  "contact_info_url": "https://dummy_contact_info_url/",
  "supported_wes_versions": [
    "v1.0.0"
  ],
  "workflow_engines": [
    {
      "engine_name": "cwltool",
      "engine_version": "1.0.20181201184214",
      "workflow_types": [
        {
          "language_type": "CWL",
          "language_version": "v1.0"
        }
      ]
    }
  ]
}
```

You can change the contents of response by editing `./config/service-info.yml`

### Add Workflow

You can add workflows by editing `./config/workflow-info.yml`

```shell
workflows:
  - workflow_name: trimming_and_qc
    workflow_version: 0c33f861553629b1e6fb4161686ab47670c9ed97
    workflow_location: https://raw.githubusercontent.com/suecharo/SAPPORO/master/SAPPORO-service/test/test_workflow/trimming_and_qc.cwl
    workflow_parameters_template_location: https://raw.githubusercontent.com/suecharo/SAPPORO/master/SAPPORO-service/test/test_workflow/trimming_and_qc_run_template.yml
    language_type: CWL
    language_version: v1.0
```

The explanation of each item is as follows.

- workflow_name
    - Describe freely
    - Uniquely naming in `workflow.yml`
- workflow_version
    - Describe freely
    - In the example, writing git Commit ID
- workflow_location
    - Describe the location of the workflow file
- workflow_parameters_template_location
    - Describe the location of the workflow execution parameters template file
- language\_[type|version]
    - Specify language\_[type|version] described in `service-info.yml`

---

There are input/output parameters restrictions for executable workflows. Please check `./test/test_workflow` as an example.

- If the local file is not mounted on the Docker container, you can't specify the local file path as the input parameter.
     - In the example, the input data is specified as a URL.
- Output data needs to be uploaded to the local file server or object storage.
     - Write the URL as one line in `upload_url.txt` in the execution directory.

### Manage Workflow Execution Engine, Job Scheduler

The workflow execution engine and job scheduler are abstracted in `./SAPPORO-service/run_workflow.sh`.

```shell
#!/bin/bash

function run_wf() {
  if [[ ${execution_engine} == "cwltool" ]]; then
    run_cwltool
  elif [[ ${execution_engine} == "nextflow" ]]; then
    run_nextflow
  elif [[ ${execution_engine} == "toil" ]]; then
    run_toil
  fi
}

function run_cwltool() {
  echo "RUNNING" > ${status_file}
  workflow_location=$(cat ${run_order_file} | yq -r '.workflow_location')
  cwltool --outdir ${output_dir} ${workflow_location} ${workflow_parameters_file} 1> ${stdout_file} 2> ${stderr_file} || echo "EXECUTOR_ERROR" > ${status_file}
  echo "COMPLETE" > ${status_file}
}
```

First, to install the workflow execution engine and the job scheduler in the Docker container. Edit `./Dockerfile` and rebuild it, or enter container `docker-compose exec app sh` and install directly. Then edit `./SAPPORO-service/run_workflow.sh` and `./config/service-info.yml`.

### Network

SAPPORO-service is using Flask. The network configuration is as follows.

```text
Flask <-> uwsgi <-(uWSGI protocol)-> Nginx <-(HTTP)-> Docker <-> User
```

---

As an initial setting, Nginx provides `localhost:1122` as a REST API endpoint. If you want to change the port, change the following part of `./docker-compose.yml`.

```yaml
ports:
  - 1122:80 # HERE
```

---

If you want to use SSL/TSL, edit `./config/nginx.conf`.

### Logging

The following items are output as logs.

```shell
$ ls ./log
flask.log  nginx-access.log  nginx-error.log  nginx.pid  uwsgi.log  uwsgi.pid
```

---

Logs are normally outputed to `./log`. If you want to change the output location, edit `./docker-compose.yml`.

```shell
--- docker-compose.yml  2019-03-05 22:51:04.612902487 +0900
+++ docker-compose.log.yml  2019-03-05 23:38:03.502634330 +0900
@@ -13,7 +13,7 @@
       - /tmp:/tmp
       - ./SAPPORO-service:/opt/SAPPORO-service/SAPPORO-service
       - ./config:/opt/SAPPORO-service/config
-      - ./log:/opt/SAPPORO-service/log
+      - /var/log/SAPPORO-service:/opt/SAPPORO-service/log
       - ./run:/opt/SAPPORO-service/run
     environment:
       - LOG_LEVEL=INFO # DEBUG or INFO
```

---

To change the log level, edit `./docker-compose.yml`. When set as `LOG_LEVEL=DEBUG`, traceback of Python is displayed in `./log/flask.log`.

```shell
    environment:
      - LOG_LEVEL=INFO # DEBUG or INFO
```

---

If you want log rotation of `./log/flask.log`, edit `./SAPPORO-service/app/logging_config.py`.

### Token authentication

SAPPORO-service can uses simple token authentication. Please edit `./docker-compose.yml`.

```shell
    environment:
      - ENABLE_TOKEN_AUTH=True # True or False
```

```shell
$ curl -X GET localhost:1122/service-info
{
  "msg": "Unauthorized.",
  "status_code": 401
}
```

Issuing a token is done as follows.

```shell
$ docker-compose exec app python3 /opt/SAPPORO-service/config/generate_token.py
Your Token is: Yv8hl40BoP1ogtp42SHq0cZTGzSyY3o4TV6EMloMzI0
$ docker-compose exec app python3 /opt/SAPPORO-service/config/generate_token.py
Your Token is: _pKRgNkEkPLqFBMpJSChVlvC2lmRHWlhW2UiuBWY760
```

The tokens are recorded in `./config/token_list.txt` in a line break delimited format. If you want to revoke, please edit this file. Even without using `./config/generate_token.py`, you can set the token by editing this file directly.

```shell
$ cat token_list.txt
Yv8hl40BoP1ogtp42SHq0cZTGzSyY3o4TV6EMloMzI0
_pKRgNkEkPLqFBMpJSChVlvC2lmRHWlhW2UiuBWY760
```

Token authentication is done by adding the `Authorization` header to the request.

```shell
$ curl -H 'Authorization:Yv8hl40BoP1ogtp42SHq0cZTGzSyY3o4TV6EMloMzI0' localhost:1122/service-info
{
  "auth_instructions_url": "https://dummy_auth_instructions_url/",
  "contact_info_url": "https://dummy_contact_info_url/",
  "supported_wes_versions": [
    "v1.0.0"
  ],
  "workflow_engines": [
    {
      "engine_name": "cwltool",
      "engine_version": "1.0.20181201184214",
      "workflow_types": [
        {
          "language_type": "CWL",
          "language_version": "v1.0"
        }
      ]
    }
  ]
}
```

---

When using token authentication, it is necessary to encrypt the header, so please use SSL/TLS.

### GET /runs

Using `GET /runs`, can check all batch jobs in SAPPORO-service. However, when using SAPPORO-service by an unspecified number of users, problems arises (e.g. canceling other user's batch jobs). Please edit `./docker-compose.yml` to change the setting.

```shell
    environment:
      - ENABLE_GET_RUNS=False # True or False
```

## Testing environment

### Execution Test

The Test is done using pytest and coverage.

```shell
$ cd test
$ docker-compose -f docker-compose.dev.yml up -d --build
$ docker-compose -f docker-compose.dev.yml exec app /bin/bash /opt/SAPPORO-service/test/run_test.sh
```

The result is output to `./test/coverage_html`.

### Development environment

You can develop using Flask's auto-reloading function. As a result, code changes are reflected immediately on the server. Files containing dev as the name in `./test` are used as the configuration files.

```shell
$ cd test
$ docker-compose -f docker-compose.dev.yml up -d --build
$ docker-compose -f docker-compose.dev.yml exec app /bin/bash /opt/SAPPORO-service/test/run_server.sh
```
