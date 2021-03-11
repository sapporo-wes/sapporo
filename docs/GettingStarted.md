# Sapporo: Getting Started

Authors: [Tazro Ohta](https://github.com/inutano), [Hirotaka Suetake](https://github.com/suecharo)

Here we introduce how to deploy Sapporo, an implementation of GA4GH workflow execution service (WES).

Sapporo has two components: **Sapporo-service** is an API server which actually runs workflows via workflow runners, and **Sapporo-Web** is a browser-based GUI to manage the workflow execution running on WES servers.

## Prerequisites

- Linux or Mac
- Docker
- Docker-compose

## Sapporo-service: The API server

Let's launch the server and run a workflow. First, clone the github repository:

```shell=
$ git clone https://github.com/ddbj/SAPPORO-service
```

If your machine has a customized setting for Docker and the binary is not located in the standard path `/usr/bin/docker`, you need to make a change in the `docker-compose.yml`. For example, if `which docker` on your machine returns `/usr/local/bin/docker`, change the line 11 as `/usr/local/bin/docker:/usr/bin/docker`. Make sure the right side of the colon remains as same.

*Note: if you are using macOS and Docker Desktop for Mac, for the time being you need to download the docker cli binary for Linux and mount it. Please visit [here](https://download.docker.com/linux/static/stable/x86_64/) and download a tarball, decompress, and place the binary `docker` command anywhere and mount it via the `docker-compose.yml`. This behaviour will be soon fixed so that the users don't need to edit the docker-compose.yml.*

```docker-compose.yml=
version: "3.5"
services:
  app:
    image: suecharo/sapporo-service:1.0.6
    container_name: sapporo
    volumes:
      # If you want to mount the host's `run.sh`, etc., uncomment below.
      # - ${PWD}/sapporo:/app/sapporo
      # The ones below are mounted for cwltool and DinD.
      - ${PWD}/run:${PWD}/run
      - /usr/bin/docker:/usr/bin/docker
      - /var/run/docker.sock:/var/run/docker.sock
      - /tmp:/tmp
    environment:
      # Priority: [Command Line Argument] -> [Environment Variable] -> [Default Values]
      - SAPPORO_HOST=0.0.0.0
      - SAPPORO_PORT=1122
      - SAPPORO_DEBUG=False
      - SAPPORO_RUN_DIR=${PWD}/run
      # - SAPPORO_GET_RUNS=True
      # - SAPPORO_RUN_ONLY_REGISTERED_WORKFLOWS=False
      # - SAPPORO_ACCESS_CONTROL_ALLOW_ORIGIN=*
      # - SAPPORO_URL_PREFIX=/
    ports:
      - 0.0.0.0:1122:1122
    restart: on-failure
    working_dir: /app
    command: ["sapporo"]
    networks:
      - sapporo

networks:
  sapporo:
    name: sapporo-network
```


Then run `docker-compose up` to launch the server:

```shell=
$ cd SAPPORO-service
$ docker-compose up
Creating network "sapporo-network" with the default driver
Pulling app (suecharo/sapporo-service:1.0.6)...
1.0.6: Pulling from suecharo/sapporo-service
a076a628af6f: Pull complete
a36ca90be64c: Pull complete
44f7d13c37e7: Pull complete
b0d4acfb9127: Pull complete
3c908eb8c37b: Pull complete
677659705766: Pull complete
46df9b1b0ed0: Pull complete
9dd9ceba07c7: Pull complete
9978b8a2297d: Pull complete
1bb89922aa1d: Pull complete
6ffd491b1d22: Pull complete
Digest: sha256:aadc7c99c0b81e19574283d3e89ee8974e2115bbe4badc49dd5369cf85cfa371
Status: Downloaded newer image for suecharo/sapporo-service:1.0.6
Creating sapporo ... done
Attaching to sapporo
sapporo |  * Serving Flask app "sapporo.app" (lazy loading)
sapporo |  * Environment: production
sapporo |    WARNING: This is a development server. Do not use it in a production deployment.
sapporo |    Use a production WSGI server instead.
sapporo |  * Debug mode: off
sapporo |  * Running on http://0.0.0.0:1122/ (Press CTRL+C to quit)
```

That's it! Now Sapporo-service is running on your computer with the address `localhost:1122`. Let's access the endpoint `/service-info` to get the general information of the WES (using `jq` to prettify the output json).

```shell=
$ curl -s localhost:1122/service-info | jq .
{
  "auth_instructions_url": "https://github.com/ddbj/SAPPORO-service",
  "contact_info_url": "https://github.com/ddbj/SAPPORO-service",
  "default_workflow_engine_parameters": [],
  "supported_filesystem_protocols": [
    "http",
    "https",
    "file",
    "s3"
  ],
  "supported_wes_versions": [
    "1.0.0"
  ],
  "system_state_counts": {
    "EXECUTOR_ERROR": 2,
    "RUNNING": 1
  },
  "tags": {
    "debug": false,
    "get_runs": true,
    "registered_only_mode": false,
    "run_dir": "/lustre7/home/lustre4/inutano/work/sapporo-demo/SAPPORO-service/run",
    "wes_name": "sapporo",
    "workflow_attachment": true
  },
  "workflow_engine_versions": {
    "cromwell": "50",
    "cwltool": "1.0.20191225192155",
    "ep3": "v1.0.0",
    "nextflow": "21.01.1-edge",
    "snakemake": "v5.17.0",
    "toil": "4.1.0"
  },
  "workflow_type_versions": {
    "CWL": {
      "workflow_type_version": [
        "v1.0",
        "v1.1",
        "v1.1.0-dev1"
      ]
    },
    "Nextflow": {
      "workflow_type_version": [
        "v1.0"
      ]
    }
  }
}
```

The full documentation of the API endpoints are desribed in [swagger](https://suecharo.github.io/sapporo-swagger-ui/dist/).


## Prepare to run a workflow

To run a workflow on a WES server, you need several configuration files shown below:

- a CWL workflow definition file (string, remote URL)
- a workflow parameter (file, json)
- a workflow engine parameter (file, json)
- a WES request tag file (file, json)

For workflow file, here we use our [fastq download workflow](https://github.com/pitagora-network/pitagora-cwl/tree/master/workflows/download-fastq). We will pass the remote URL of this workflow file hosted on github, but make sure to use the "raw" file URL, `https://github.com/pitagora-network/pitagora-cwl/raw/master/workflows/download-fastq/download-fastq.cwl`.

This workflow requires three inputs: A list of Sequence Read Archive Run ID, the source repository, and the number of threads. Here we describe these input parameters as follows in a json file named `workflow_params.json`.

```workflow_params.json=
{
  "run_ids": [
    "SRR1274307"
  ],
  "repo": "ebi",
  "nthreads": 4
}
```

Next, we can specify the workflow engine parameters, but we remain it empty. We can put an empty JSON object to the file named `workflow_engine_parameters.json`.

```shell=
$ cat workflow_engine_parameters.json
{}
```

The last file called "tag file" is to specify the tags bound to this run, which passes the optional arguments to the WES server. Tags can control the behaviour of the WES which would be different depending on the implementation.

Sapporo does not give the output file to users via the local file system: instead, it transfers the output file to the server specified by the user. For now Sapporo supports only the S3 protocol. Users need to declare the location of object storage, security credentials, and bucket information by using the tag file.

In this demo we use the minio playground as a destination. The minio playground provides public credentials for testing purpose. The tag file looks as below:

```tags.json=
{
  "export_output": {
    "protocol": "s3",
    "endpoint": "https://play.min.io:9000",
    "access_key": "Q3AM3UQ867SPQQA43P2F",
    "secret_access_key": "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
    "bucket_name": "0000-sapporo-demo",
    "dirname": "sapporo-demo-output-dir"
  }
}
```

Now you are ready to run a workflow!

## POST to run a workflow

Using curl to post a request to run a workflow with the files we prepared. The server returns a json object which contains a `run_id`, an identifier for this workflow run.

```curl=
$ curl -s -X POST \
   -F "workflow_url=https://github.com/pitagora-network/pitagora-cwl/raw/master/workflows/download-fastq/download-fastq.cwl" \
   -F "workflow_type=CWL" \
   -F "workflow_type_version=v1.0" \
   -F "workflow_params=<workflow_params.json" \
   -F "workflow_engine_name=cwltool" \
   -F "workflow_engine_parameters=<workflow_engine_parameters.json" \
   -F "tags=<tags.json" \
   http://localhost:1122/runs
{"run_id":"b4989888-8628-439f-ae67-fd7d3e08491b"}
```

Next we ask the status of the run by using the `run_id`.

```curl=
$ curl -s localhost:1122/runs/b4989888-8628-439f-ae67-fd7d3e08491b | jq .
{
  "outputs": null,
  "request": {
    "tags": "{\n  \"export_output\": {\n    \"protocol\": \"s3\",\n    \"endpoint\": \"https://play.min.io:9000\",\n    \"access_key\": \"Q3AM3UQ867SPQQA43P2F\",\n    \"secret_access_key\": \
"zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG\",\n    \"bucket_name\": \"0000-sapporo-demo\",\n    \"dirname\": \"sapporo-demo-output-dir\"\n  }\n}",
    "workflow_attachment": [],
    "workflow_engine_name": "cwltool",
    "workflow_engine_parameters": "{}",
    "workflow_name": "download-fastq.cwl",
    "workflow_params": "{\n  \"run_ids\": [\n    \"SRR1274307\"\n  ],\n  \"repo\": \"ebi\",\n  \"nthreads\": 4\n}\n",
    "workflow_type": "CWL",
    "workflow_type_version": "v1.0",
    "workflow_url": "https://github.com/pitagora-network/pitagora-cwl/raw/master/workflows/download-fastq/download-fastq.cwl"
  },
  "run_id": "b4989888-8628-439f-ae67-fd7d3e08491b",
  "run_log": {
    "cmd": "docker run -i --rm -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp -v /Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b:/Users/inutano/work
/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b -w=/Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/exe commonworkflowlanguage/cwltool:1.0.20191225
192155 --outdir /Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/outputs https://github.com/pitagora-network/pitagora-cwl/raw/master/workflows/download-fastq/do
wnload-fastq.cwl /Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/exe/workflow_params.json 1>/Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-
fd7d3e08491b/stdout.log 2>/Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/stderr.log",
    "end_time": null,
    "exit_code": null,
    "name": "download-fastq.cwl",
    "start_time": "2021-02-03T03:19:27",
    "stderr": "Unable to find image 'commonworkflowlanguage/cwltool:1.0.20191225192155' locally\n1.0.20191225192155: Pulling from commonworkflowlanguage/cwltool\n89d9c30c1d48: Pulling fs laye
r\n910c49c00810: Pulling fs layer\n356e2b6f7f7c: Pulling fs layer\ne2700c1bbf1f: Pulling fs layer\nb644b1801e4a: Pulling fs layer\n1d6b5ae58845: Pulling fs layer\nda3d895d61d1: Pulling fs lay
er\n98fc897dedbe: Pulling fs layer\nee864c691a1d: Pulling fs layer\n1d6b5ae58845: Waiting\n98fc897dedbe: Waiting\nda3d895d61d1: Waiting\ne2700c1bbf1f: Waiting\nb644b1801e4a: Waiting\n910c49c0
0810: Verifying Checksum\n910c49c00810: Download complete\n89d9c30c1d48: Pull complete\n356e2b6f7f7c: Verifying Checksum\n356e2b6f7f7c: Download complete\n910c49c00810: Pull complete\ne2700c1
bbf1f: Verifying Checksum\ne2700c1bbf1f: Download complete\nb644b1801e4a: Verifying Checksum\nb644b1801e4a: Download complete\n98fc897dedbe: Verifying Checksum\n98fc897dedbe: Download complet
e\n356e2b6f7f7c: Pull complete\ne2700c1bbf1f: Pull complete\nb644b1801e4a: Pull complete\nee864c691a1d: Download complete\nda3d895d61d1: Verifying Checksum\nda3d895d61d1: Download complete\n1
d6b5ae58845: Download complete\n1d6b5ae58845: Pull complete\nda3d895d61d1: Pull complete\n98fc897dedbe: Pull complete\nee864c691a1d: Pull complete\nDigest: sha256:3119afc0693ce5231165708b8e99c16101f82a8853d57698049bf23ed2fa2e05\nStatus: Downloaded newer image for commonworkflowlanguage/cwltool:1.0.20191225192155\n\u001b[1;30mINFO\u001b[0m /usr/local/bin/cwltool 1.0.20191225192155\n",
    "stdout": ""
  },
  "state": "RUNNING",
  "task_logs": null
}
```

It is running! Wait for seconds, and again:

```curl=
$ curl -s localhost:1122/runs/b4989888-8628-439f-ae67-fd7d3e08491b | jq .
{
  "outputs": {
    "SRR1274307_1.fastq.gz": "/Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/outputs/SRR1274307_1.fastq.gz",
    "SRR1274307_2.fastq.gz": "/Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/outputs/SRR1274307_2.fastq.gz"
  },
  "request": {
    "tags": "{\n  \"export_output\": {\n    \"protocol\": \"s3\",\n    \"endpoint\": \"https://play.min.io:9000\",\n    \"access_key\": \"Q3AM3UQ867SPQQA43P2F\",\n    \"secret_access_key\": \
"zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG\",\n    \"bucket_name\": \"0000-sapporo-demo\",\n    \"dirname\": \"sapporo-demo-output-dir\"\n  }\n}",
    "workflow_attachment": [],
    "workflow_engine_name": "cwltool",
    "workflow_engine_parameters": "{}",
    "workflow_name": "download-fastq.cwl",
    "workflow_params": "{\n  \"run_ids\": [\n    \"SRR1274307\"\n  ],\n  \"repo\": \"ebi\",\n  \"nthreads\": 4\n}\n",
    "workflow_type": "CWL",
    "workflow_type_version": "v1.0",
    "workflow_url": "https://github.com/pitagora-network/pitagora-cwl/raw/master/workflows/download-fastq/download-fastq.cwl"
  },
  "run_id": "b4989888-8628-439f-ae67-fd7d3e08491b",
  "run_log": {
    "cmd": "docker run -i --rm -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp -v /Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b:/Users/inutano/work
/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b -w=/Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/exe commonworkflowlanguage/cwltool:1.0.20191225
192155 --outdir /Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/outputs https://github.com/pitagora-network/pitagora-cwl/raw/master/workflows/download-fastq/do
wnload-fastq.cwl /Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/exe/workflow_params.json 1>/Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-
fd7d3e08491b/stdout.log 2>/Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/stderr.log",
    "end_time": "2021-02-03T03:20:59",
    "exit_code": 0,
    "name": "download-fastq.cwl",
    "start_time": "2021-02-03T03:19:27",
"stderr": "Unable to find image 'commonworkflowlanguage/cwltool:1.0.20191225192155' locally\n1.0.20191225192155: Pulling from commonworkflowlanguage/cwltool\n89d9c30c1d48: Pullin[18/1875]
r\n910c49c00810: Pulling fs layer\n356e2b6f7f7c: Pulling fs layer\ne2700c1bbf1f: Pulling fs layer\nb644b1801e4a: Pulling fs layer\n1d6b5ae58845: Pulling fs layer\nda3d895d61d1: Pulling fs lay
er\n98fc897dedbe: Pulling fs layer\nee864c691a1d: Pulling fs layer\n1d6b5ae58845: Waiting\n98fc897dedbe: Waiting\nda3d895d61d1: Waiting\ne2700c1bbf1f: Waiting\nb644b1801e4a: Waiting\n910c49c0
0810: Verifying Checksum\n910c49c00810: Download complete\n89d9c30c1d48: Pull complete\n356e2b6f7f7c: Verifying Checksum\n356e2b6f7f7c: Download complete\n910c49c00810: Pull complete\ne2700c1
bbf1f: Verifying Checksum\ne2700c1bbf1f: Download complete\nb644b1801e4a: Verifying Checksum\nb644b1801e4a: Download complete\n98fc897dedbe: Verifying Checksum\n98fc897dedbe: Download complet
e\n356e2b6f7f7c: Pull complete\ne2700c1bbf1f: Pull complete\nb644b1801e4a: Pull complete\nee864c691a1d: Download complete\nda3d895d61d1: Verifying Checksum\nda3d895d61d1: Download complete\n1
d6b5ae58845: Download complete\n1d6b5ae58845: Pull complete\nda3d895d61d1: Pull complete\n98fc897dedbe: Pull complete\nee864c691a1d: Pull complete\nDigest: sha256:3119afc0693ce5231165708b8e99
c16101f82a8853d57698049bf23ed2fa2e05\nStatus: Downloaded newer image for commonworkflowlanguage/cwltool:1.0.20191225192155\n\u001b[1;30mINFO\u001b[0m /usr/local/bin/cwltool 1.0.20191225192155
\nCould not load extension schema https://schema.org/docs/schema_org_rdfa.html: None:11:92: Repeat node-elements inside property elements: http://www.w3.org/1999/xhtmlmeta\n\u001b[1;30mWARNIN
G\u001b[0m \u001b[33mWorkflow checker warning:\nhttps://github.com/pitagora-network/pitagora-cwl/raw/master/workflows/download-fastq/download-fastq.cwl:12:5: Source 'nthreads'\n
                                                                                                of type [\"null\",\n
                                   \"int\"] may be\n                                                                                                              incompatible\nhttps://github.
com/pitagora-network/pitagora-cwl/raw/master/workflows/download-fastq/download-fastq.cwl:39:7:   with sink\n
                             'nthreads' of type\n                                                                                                                \"int\"\nhttps://github.com/pi
tagora-network/pitagora-cwl/raw/master/workflows/download-fastq/download-fastq.cwl:17:5: Source 'repo' of\n
                          type [\"null\",\n                                                                                                              \"string\"] may be\n
                                                                                            incompatible\nhttps://github.com/pitagora-network/pitagora-cwl/raw/master/workflows/download-fastq/
download-fastq.cwl:31:7:   with sink 'repo'\n                                                                                                                of type \"string\"\u001b[0m\n\u001
b[1;30mINFO\u001b[0m [workflow ] start\n\u001b[1;30mINFO\u001b[0m [workflow ] starting step download_sra\n\u001b[1;30mINFO\u001b[0m [step download_sra] start\n\u001b[1;30mINFO\u001b[0m ['dock
er', 'pull', 'quay.io/inutano/download-sra:0.2.1']\n0.2.1: Pulling from inutano/download-sra\n5d20c808ce19: Pulling fs layer\n26033daab2b1: Pulling fs layer\n6936ed840dfa: Pulling fs layer\n6
936ed840dfa: Verifying Checksum\n6936ed840dfa: Download complete\n26033daab2b1: Verifying Checksum\n26033daab2b1: Download complete\n5d20c808ce19: Verifying Checksum\n5d20c808ce19: Pull compl
ete\n26033daab2b1: Pull complete\n6936ed840dfa: Pull complete\nDigest: sha256:69f1ca73377435be390bffede86219f3a5c4aa63aeb7b8041089a77a22d75027\nStatus: Downloaded newer image for quay.io/inut
ano/download-sra:0.2.1\n\u001b[1;30mINFO\u001b[0m [job download_sra] /tmp/sr4twlg5$ docker \\\n    run \\\n    -i \\\n    --volume=/tmp/sr4twlg5:/LnmKAL:rw \\\n    --volume=/tmp/ozwnhabd:/tmp
:rw \\\n    --workdir=/LnmKAL \\\n    --read-only=true \\\n    --user=0:0 \\\n    --rm \\\n    --env=TMPDIR=/tmp \\\n    --env=HOME=/LnmKAL \\\n    --cidfile=/tmp/a0bf_mqj/20210203032004-2735
43.cid \\\n    quay.io/inutano/download-sra:0.2.1 \\\n    download-sra \\\n    -r \\\n    ebi \\\n    SRR1274307\n--2021-02-03 03:20:04--  ftp://ftp.sra.ebi.ac.uk/vol1/srr/SRR127/007/SRR12743
07\n           => 'SRR1274307.sra'\nResolving ftp.sra.ebi.ac.uk... 193.62.193.138\nConnecting to ftp.sra.ebi.ac.uk|193.62.193.138|:21... connected.\nLogging in as anonymous ... Logged in!\n==
> SYST ... done.    ==> PWD ... done.\n==> TYPE I ... done.  ==> CWD (1) /vol1/srr/SRR127/007 ... done.\n==> SIZE SRR1274307 ... 946479\n==> PASV ... done.    ==> RETR SRR1274307 ... done.\nL
ength: 946479 (924K) (unauthoritative)\n\n     0K .......... .......... .......... .......... ..........  5% 90.1K 10s\n    50K .......... .......... .......... .......... .......... 10%  200
K 7s\n   100K .......... .......... .......... .......... .......... 16%  201K 5s\n   150K .......... .......... .......... .......... .......... 21% 5.47M 4s\n   200K .......... .......... .
......... .......... .......... 27%  201K 4s\n   250K .......... .......... .......... .......... .......... 32%  204K 3s\n   300K .......... .......... .......... .......... .......... 37%
204K 3s\n   350K .......... .......... .......... .......... .......... 43%  202K 3s\n   400K .......... .......... .......... .......... .......... 48% 5.54M 2s\n   450K .......... .........
. .......... .......... .......... 54%  162K 2s\n   500K .......... .......... .......... .......... .......... 59%  205K 2s\n   550K .......... .......... .......... .......... .......... 64
% 4.10M 1s\n   600K .......... .......... .......... .......... .......... 70%  206K 1s\n   650K .......... .......... .......... .......... .......... 75%  208K 1s\n   700K .......... ......
.... .......... .......... .......... 81% 4.30M 1s\n   750K .......... .......... .......... .......... .......... 86%  208K 1s\n   800K .......... .......... .......... .......... ..........
 91% 5.37M 0s\n   850K .......... .......... .......... .......... .......... 97%  207K 0s\n   900K .......... .......... ....                            100% 7.80M=3.6s\n\n2021-02-03 03:20:1
1 (256 KB/s) - 'SRR1274307.sra' saved [946479]\n\n\u001b[1;30mINFO\u001b[0m [job download_sra] Max memory used: 1MiB\n\u001b[1;30mINFO\u001b[0m [job download_sra] completed success\n\u001b[1;
30mINFO\u001b[0m [step download_sra] completed success\n\u001b[1;30mINFO\u001b[0m [workflow ] starting step pfastq_dump\n\u001b[1;30mINFO\u001b[0m [step pfastq_dump] start\n\u001b[1;30mINFO\u
001b[0m ['docker', 'pull', 'quay.io/inutano/sra-toolkit:v2.9.0']\nv2.9.0: Pulling from inutano/sra-toolkit\nd8d1b9d0fad7: Pulling fs layer\nff8923c0c81d: Pulling fs layer\na0e4bf411830: Pulli
ng fs layer\nfe23b5934555: Pulling fs layer\n9cbeb98e2f73: Pulling fs layer\ne4d6e1f8f7b0: Pulling fs layer\n184ea3f39f9e: Pulling fs layer\n9333b8d7b119: Pulling fs layer\nde906d5248f0: Pull
ing fs layer\n9cbeb98e2f73: Waiting\ne4d6e1f8f7b0: Waiting\n184ea3f39f9e: Waiting\n9333b8d7b119: Waiting\nde906d5248f0: Waiting\nfe23b5934555: Waiting\nff8923c0c81d: Download complete\na0e4bf
411830: Verifying Checksum\na0e4bf411830: Download complete\nfe23b5934555: Verifying Checksum\nfe23b5934555: Download complete\n9cbeb98e2f73: Download complete\nd8d1b9d0fad7: Verifying Checks
um\nd8d1b9d0fad7: Download complete\ne4d6e1f8f7b0: Verifying Checksum\ne4d6e1f8f7b0: Download complete\n9333b8d7b119: Verifying Checksum\n9333b8d7b119: Download complete\nde906d5248f0: Verify
ing Checksum\nde906d5248f0: Download complete\nd8d1b9d0fad7: Pull complete\nff8923c0c81d: Pull complete\na0e4bf411830: Pull complete\nfe23b5934555: Pull complete\n9cbeb98e2f73: Pull complete\
ne4d6e1f8f7b0: Pull complete\n184ea3f39f9e: Verifying Checksum\n184ea3f39f9e: Download complete\n184ea3f39f9e: Pull complete\n9333b8d7b119: Pull complete\nde906d5248f0: Pull complete\nDigest:
 sha256:6fd4a55d66354ec14c363888fdc44ebac4531a263b00f799c810064cd6a591f2\nStatus: Downloaded newer image for quay.io/inutano/sra-toolkit:v2.9.0\n\u001b[1;30mINFO\u001b[0m [job pfastq_dump] /t
mp/zkdmni53$ docker \\\n    run \\\n    -i \\\n    --volume=/tmp/zkdmni53:/LnmKAL:rw \\\n    --volume=/tmp/vx8fa64g:/tmp:rw \\\n    --volume=/tmp/sr4twlg5/SRR1274307.sra:/var/lib/cwl/stgb8355
1f0-e2ec-4b42-8c77-c08bab8b35cc/SRR1274307.sra:ro \\\n    --workdir=/LnmKAL \\\n    --read-only=true \\\n    --user=0:0 \\\n    --rm \\\n    --env=TMPDIR=/tmp \\\n    --env=HOME=/LnmKAL \\\n
   --cidfile=/tmp/k457o5e6/20210203032034-901817.cid \\\n    quay.io/inutano/sra-toolkit:v2.9.0 \\\n    pfastq-dump \\\n    --gzip \\\n    -t \\\n    4 \\\n    --readids \\\n    --skip-techni
cal \\\n    --split-files \\\n    --split-spot \\\n    /var/lib/cwl/stgb83551f0-e2ec-4b42-8c77-c08bab8b35cc/SRR1274307.sra\nUsing sra-stat : 2.9.0\nUsing fastq-dump : 2.9.0\ntmpdir: /LnmKAL\
   --cidfile=/tmp/k457o5e6/20210203032034-901817.cid \\\n    quay.io/inutano/sra-toolkit:v2.9.0 \\\n    pfastq-dump \\\n    --gzip \\\n    -t \\\n    4 \\\n    --readids \\\n    --skip-techni
cal \\\n    --split-files \\\n    --split-spot \\\n    /var/lib/cwl/stgb83551f0-e2ec-4b42-8c77-c08bab8b35cc/SRR1274307.sra\nUsing sra-stat : 2.9.0\nUsing fastq-dump : 2.9.0\ntmpdir: /LnmKAL\n
outdir: /LnmKAL\nblocks: 1,6846 6847,13692 13693,20538 20539,27386\nRead 6846 spots for /var/lib/cwl/stgb83551f0-e2ec-4b42-8c77-c08bab8b35cc/SRR1274307.sra\nWritten 6846 spots for /var/lib/cw
l/stgb83551f0-e2ec-4b42-8c77-c08bab8b35cc/SRR1274307.sra\nRead 6846 spots for /var/lib/cwl/stgb83551f0-e2ec-4b42-8c77-c08bab8b35cc/SRR1274307.sra\nWritten 6846 spots for /var/lib/cwl/stgb8355
1f0-e2ec-4b42-8c77-c08bab8b35cc/SRR1274307.sra\nRead 6846 spots for /var/lib/cwl/stgb83551f0-e2ec-4b42-8c77-c08bab8b35cc/SRR1274307.sra\nWritten 6846 spots for /var/lib/cwl/stgb83551f0-e2ec-4
b42-8c77-c08bab8b35cc/SRR1274307.sra\nRead 6848 spots for /var/lib/cwl/stgb83551f0-e2ec-4b42-8c77-c08bab8b35cc/SRR1274307.sra\nWritten 6848 spots for /var/lib/cwl/stgb83551f0-e2ec-4b42-8c77-c
08bab8b35cc/SRR1274307.sra\n\u001b[1;30mINFO\u001b[0m [job pfastq_dump] Max memory used: 0MiB\n\u001b[1;30mINFO\u001b[0m [job pfastq_dump] completed success\n\u001b[1;30mINFO\u001b[0m [step p
fastq_dump] completed success\n\u001b[1;30mINFO\u001b[0m [workflow ] completed success\n\u001b[1;30mINFO\u001b[0m Final process status is success\n",
    "stdout": "{\n    \"fastq_files\": [\n        {\n            \"location\": \"file:///Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/outputs/SRR1274307_1.fa
stq.gz\",\n            \"basename\": \"SRR1274307_1.fastq.gz\",\n            \"class\": \"File\",\n            \"checksum\": \"sha1$22f01534b704d7024f36ce95cf975be80f4dda54\",\n            \"
size\": 736698,\n            \"format\": \"http://edamontology.org/format_1930\",\n            \"path\": \"/Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/outp
uts/SRR1274307_1.fastq.gz\"\n        },\n        {\n            \"location\": \"file:///Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/outputs/SRR1274307_2.fas
tq.gz\",\n            \"basename\": \"SRR1274307_2.fastq.gz\",\n            \"class\": \"File\",\n            \"checksum\": \"sha1$c381b2fc6c3783716c5c0fe645a4df27b0006251\",\n            \"s
ize\": 761425,\n            \"format\": \"http://edamontology.org/format_1930\",\n            \"path\": \"/Users/inutano/work/SAPPORO-service/run/b4/b4989888-8628-439f-ae67-fd7d3e08491b/outpu
ts/SRR1274307_2.fastq.gz\"\n        }\n    ]\n}\n"
  },
  "state": "COMPLETE",
  "task_logs": null
}
```

The `state` turned to `"COMPLETE"`, now it's done! Let's see if the output is correctly transfered the minio playground, open https://play.min.io:9000/minio/0000-sapporo-demo/ to check the outputs:

![](https://i.imgur.com/ss0gJqk.png)

Woohoo! :tada: Now you successfully deployed your own CWL-as-a-Service!


## SAPPORO-web: A GUI for WES endpoint

Next we try to use SAPPORO-web, a web-based GUI application that allows users to run and manage workflows on a WES server. SAPPORO-web is implemented as a javascript SPA and hosted on GitHub pages. You can access https://ddbj.github.io/SAPPORO-web/ or you can deploy your own SAPPORO-web. See details at https://github.com/ddbj/SAPPORO-web .

![](https://i.imgur.com/dxPx3UF.png)


Here we use the one on GitHub pages. First, we need to register a WES endpoint we are going to use. Click the register button and input the address and the name for this endpoint. This time we input the localhost address `http://localhost:1122`, but make sure to use https protocol to avoid mixed content error if you try with your own server.

![](https://i.imgur.com/15LkBW1.jpg)

If the server is successfully registered, the `service-info` will be shown up. 

![](https://i.imgur.com/JUT2Kr1.jpg)

Next, we need to register a workflow to run on the server. Click register in the box of the workflow and input the URL we used above: `https://github.com/pitagora-network/pitagora-cwl/raw/master/workflows/download-fastq/download-fastq.cwl` .

![](https://i.imgur.com/kaCxLy1.jpg)

If the workflow is successfully registered, the workflow details and the form to input the parameters will appear.

![](https://i.imgur.com/HGzBcpo.jpg)

Here we input the same parameters we used.

![](https://i.imgur.com/Bw71W9K.jpg)

*Note: current SAPPORO-web implementation cannot handle the array input on the automatically generated input parameter form, will be supported soon*

After a while, click the reload button next to the status badge.

![](https://i.imgur.com/LaWYJ34.jpg)

It's done again! Visit the play.min.io and see if the output files are created.

## Sapporo needs your help!

The [DDBJ](https://ddbj.nig.ac.jp) has maintained a shared computing cluster for over 10 years. The demand that we often asked by the users is to share the tools and the workflows among the other users with ease.

A year ago we made the first release of Sapporo. We have been dogfooding to investigate if the application suits our purpose. Now we published the major update, including the new features for both Sapporo-service and Sapporo-web. Sapporo-service is now a full implementation of the GA4GH WES standard, and ready for production deployment. Sapporo-web is yet under the development and may have bugs (we found some while creating this tutorial document, oo!). Please try deploying Sapporo on your computer and run your workflows, and let us know what you think. Of course we welcome your pull request to [github/ddbj/Sapporo-service](https://github.com/ddbj/SAPPORO-service) or [github/ddbj/Sapporo-web](https://github/ddbj/Sapporo-web) ! 

## Acknowledgement

The development of Sapporo is supported by [DDBJ](https://ddbj.nig.ac.jp). We thank the members of the two user groups, the [pitagora network](https://pitagora-network.org/) and the [workflow meetup Japan](https://workflow-meetup-jp.github.io/). This work is partially supported by the CREST program of the Japan Science and Technology Agency (grant No. JPMJCR1501).
