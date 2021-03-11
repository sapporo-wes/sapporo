# Sapporo: Getting Started

Authors: [Tazro Ohta](https://github.com/inutano), [Hirotaka Suetake](https://github.com/suecharo)

Here we introduce how to deploy Sapporo, an implementation of GA4GH workflow execution service (WES).

Sapporo has two components: **Sapporo-Service** is an API server which actually runs workflows via workflow runners, and **Sapporo-Web** is a browser-based GUI to manage the workflow execution running on WES servers.

## Prerequisites

- Linux or Mac
- Docker
- docker-compose

## Sapporo-service: The API server

Let's launch the server and run a workflow. First, clone the github repository:

```shell=
$ git clone https://github.com/ddbj/SAPPORO-service
```

Then run `docker-compose up` to launch the server:

```shell=
$ cd SAPPORO-service
$ docker-compose up
Creating network "sapporo-network" with the default driver
Pulling app (ghcr.io/ddbj/sapporo-service:1.0.11)...
1.0.11: Pulling from ddbj/sapporo-service
45b42c59be33: Already exists
f875e16ab19c: Already exists
cbef73715c9a: Already exists
8ad3aa474633: Already exists
847bc7dff64c: Already exists
7790517fdc09: Pull complete
9c33c2d75472: Pull complete
2d9680598ed7: Pull complete
28fb56cb400e: Pull complete
221cafaac757: Pull complete
c79371995952: Pull complete
6f574dedcd9e: Pull complete
2a4e81ede1af: Pull complete
Recreating sapporo ... done
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
  "executable_workflows": [...],
  "supported_filesystem_protocols": [
    "http",
    "https",
    "file",
    "s3"
  ],
  "supported_wes_versions": [
    "sapporo-wes-1.0.0"
  ],
  "system_state_counts": {},
  "tags": {
    "debug": false,
    "get_runs": true,
    "registered_only_mode": false,
    "wes_name": "sapporo",
    "workflow_attachment": true
  },
  "workflow_engine_versions": {
    "cromwell": "55",
    "cwltool": "1.0.20191225192155",
    "ep3 (experimental)": "v1.0.0",
    "nextflow": "21.01.1-edge",
    "snakemake": "v5.32.0",
    "toil (experimental)": "4.1.0"
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
    },
    "Snakemake": {
      "workflow_type_version": [
        "v1.0"
      ]
    },
    "WDL": {
      "workflow_type_version": [
        "1.0"
      ]
    }
  }
}
```

The full documentation of the API endpoints are desribed in [Swagger UI - Sapporo-Service](https://suecharo.github.io/sapporo-swagger-ui/dist/).

## Prepare to run a workflow

To run a workflow on a WES server, you need several configuration files shown below:

- a CWL workflow definition file (string, remote URL)
- a workflow parameter (file, json)
- a workflow engine parameter (file, json)
- a WES request tag file (file, json)

For workflow file, here we use our [fastq download workflow](https://github.com/pitagora-network/pitagora-cwl/tree/master/workflows/download-fastq). We will pass the remote URL of this workflow file hosted on github, but make sure to use the "raw" file URL, `https://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl`.

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

```shell=
$ cat tags.json
{}
```

Now you are ready to run a workflow!

## POST to run a workflow

Using curl to post a request to run a workflow with the files we prepared. The server returns a json object which contains a `run_id`, an identifier for this workflow run.

```curl=
$ curl -s -X POST \
    -F "workflow_url=https://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl" \
    -F "workflow_type=CWL" \
    -F "workflow_type_version=v1.0" \
    -F "workflow_params=<workflow_params.json" \
    -F "workflow_engine_name=cwltool" \
    -F "workflow_engine_parameters=<workflow_engine_parameters.json" \
    -F "tags=<tags.json" \
    http://localhost:1122/runs
{"run_id":"98a99495-2a3a-40ce-b033-46ad01ab0044"}
```

Next we ask the status of the run by using the `run_id`.

```curl=
$ curl -s localhost:1122/runs/98a99495-2a3a-40ce-b033-46ad01ab0044 | jq .
{
  "outputs": null,
  "request": {
    "tags": "{}\n",
    "workflow_attachment": [],
    "workflow_engine_name": "cwltool",
    "workflow_engine_parameters": "{}\n",
    "workflow_name": "download-fastq.cwl",
    "workflow_params": "{\n  \"run_ids\": [\n    \"SRR1274307\"\n  ],\n  \"repo\": \"ebi\",\n  \"nthreads\": 4\n}\n",
    "workflow_type": "CWL",
    "workflow_type_version": "v1.0",
    "workflow_url": "https://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl"
  },
  "run_id": "98a99495-2a3a-40ce-b033-46ad01ab0044",
  "run_log": {
    "cmd": "docker run -i --rm -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp -v /home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044:/home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044 -w=/home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/exe commonworkflowlanguage/cwltool:1.0.20191225192155 --outdir /home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/outputs https://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl /home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/exe/workflow_params.json 1>/home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/stdout.log 2>/home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/stderr.log",
    "end_time": null,
    "exit_code": null,
    "name": "download-fastq.cwl",
    "start_time": "2021-03-11T22:19:53",
    "stderr": "\u001b[1;30mINFO\u001b[0m /usr/local/bin/cwltool 1.0.20191225192155\nCould not load extension schema https://schema.org/docs/schema_org_rdfa.html: None:11:92: Repeat node-elements inside property elements: http://www.w3.org/1999/xhtmlmeta\n\u001b[1;30mWARNING\u001b[0m \u001b[33mWorkflow checker warning:\nhttps://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl:14:5: Source 'nthreads'\n                                                                                                                         of type [\"null\",\n                                                                                                                         \"int\"] may be\n                                                                                                                         incompatible\nhttps://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl:41:7:   with sink\n                                                                                                                           'nthreads' of type\n                                                                                                                           \"int\"\nhttps://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl:19:5: Source 'repo' of\n                                                                                                                         type [\"null\",\n                                                                                                                         \"string\"] may be\n                                                                                                                         incompatible\nhttps://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl:33:7:   with sink 'repo'\n                                                                                                                           of type \"string\"\u001b[0m\n\u001b[1;30mINFO\u001b[0m [workflow ] start\n\u001b[1;30mINFO\u001b[0m [workflow ] starting step download_sra\n\u001b[1;30mINFO\u001b[0m [step download_sra] start\n\u001b[1;30mINFO\u001b[0m ['docker', 'pull', 'quay.io/inutano/download-sra:0.2.1']\n0.2.1: Pulling from inutano/download-sra\n5d20c808ce19: Pulling fs layer\n26033daab2b1: Pulling fs layer\n6936ed840dfa: Pulling fs layer\n5d20c808ce19: Download complete\n5d20c808ce19: Pull complete\n6936ed840dfa: Verifying Checksum\n6936ed840dfa: Download complete\n26033daab2b1: Verifying Checksum\n26033daab2b1: Download complete\n26033daab2b1: Pull complete\n6936ed840dfa: Pull complete\nDigest: sha256:69f1ca73377435be390bffede86219f3a5c4aa63aeb7b8041089a77a22d75027\nStatus: Downloaded newer image for quay.io/inutano/download-sra:0.2.1\n\u001b[1;30mINFO\u001b[0m [job download_sra] /tmp/1k8ba4u6$ docker \\\n    run \\\n    -i \\\n    --volume=/tmp/1k8ba4u6:/ebxWvx:rw \\\n    --volume=/tmp/pmjhk0_d:/tmp:rw \\\n    --workdir=/ebxWvx \\\n    --read-only=true \\\n    --user=0:0 \\\n    --rm \\\n    --env=TMPDIR=/tmp \\\n    --env=HOME=/ebxWvx \\\n    --cidfile=/tmp/uupe_aud/20210311222022-280547.cid \\\n    quay.io/inutano/download-sra:0.2.1 \\\n    download-sra \\\n    -r \\\n    ebi \\\n    SRR1274307\n--2021-03-11 22:20:23--  ftp://ftp.sra.ebi.ac.uk/vol1/srr/SRR127/007/SRR1274307\n           => 'SRR1274307.sra'\nResolving ftp.sra.ebi.ac.uk... 193.62.197.74\nConnecting to ftp.sra.ebi.ac.uk|193.62.197.74|:21... connected.\nLogging in as anonymous ... Logged in!\n==> SYST ... done.    ==> PWD ... done.\n==> TYPE I ... done.  ==> CWD (1) /vol1/srr/SRR127/007 ... done.\n==> SIZE SRR1274307 ... 946479\n==> PASV ... done.    ==> RETR SRR1274307 ... done.\nLength: 946479 (924K) (unauthoritative)\n\n     0K .......... .......... .......... .......... ..........  5% 80.8K 11s\n    50K .......... .......... .......... .......... .......... 10%  213K 7s\n   100K .......... .......... .......... .......... .......... 16% 30.5M 4s\n   150K .......... .......... .......... .......... .......... 21% 9.68M 3s\n   200K .......... .......... .......... .......... .......... 27%  219K 3s\n   250K .......... .......... .......... .......... .......... 32% 16.3M 2s\n   300K .......... .......... .......... .......... .......... 37% 11.2M 2s\n   350K .......... .......... .......... .......... .......... 43% 8.14M 1s\n   400K .......... .......... .......... .......... .......... 48%  227K 1s\n   450K .......... .......... .......... .......... .......... 54% 34.5M 1s\n   500K .......... .......... .......... .......... .......... 59% 40.9M 1s\n   550K .......... .......... .......... .......... .......... 64% 49.6M 1s\n   600K .......... .......... .......... .......... .......... 70% 36.6M 1s\n   650K .......... .......... .......... .......... .......... 75% 20.0M 0s\n   700K .......... .......... .......... .......... .......... 81% 16.2M 0s\n   750K .......... .......... .......... .......... .......... 86% 17.4M 0s\n   800K .......... .......... .......... .......... .......... 91%  226K 0s\n   850K .......... .......... .......... .......... .......... 97% 32.9M 0s\n   900K .......... .......... ....                            100% 11.9M=1.6s\n\n2021-03-11 22:20:29 (592 KB/s) - 'SRR1274307.sra' saved [946479]\n\n\u001b[1;30mINFO\u001b[0m [job download_sra] Max memory used: 1MiB\n\u001b[1;30mINFO\u001b[0m [job download_sra] completed success\n\u001b[1;30mINFO\u001b[0m [step download_sra] completed success\n\u001b[1;30mINFO\u001b[0m [workflow ] starting step pfastq_dump\n\u001b[1;30mINFO\u001b[0m [step pfastq_dump] start\n\u001b[1;30mINFO\u001b[0m ['docker', 'pull', 'quay.io/inutano/sra-toolkit:v2.9.0']\nv2.9.0: Pulling from inutano/sra-toolkit\nd8d1b9d0fad7: Pulling fs layer\nff8923c0c81d: Pulling fs layer\na0e4bf411830: Pulling fs layer\nfe23b5934555: Pulling fs layer\n9cbeb98e2f73: Pulling fs layer\ne4d6e1f8f7b0: Pulling fs layer\n184ea3f39f9e: Pulling fs layer\n9333b8d7b119: Pulling fs layer\nde906d5248f0: Pulling fs layer\nfe23b5934555: Waiting\n9cbeb98e2f73: Waiting\ne4d6e1f8f7b0: Waiting\n184ea3f39f9e: Waiting\n9333b8d7b119: Waiting\nde906d5248f0: Waiting\na0e4bf411830: Verifying Checksum\na0e4bf411830: Download complete\nff8923c0c81d: Verifying Checksum\nff8923c0c81d: Download complete\nfe23b5934555: Verifying Checksum\nfe23b5934555: Download complete\n9cbeb98e2f73: Verifying Checksum\n9cbeb98e2f73: Download complete\nd8d1b9d0fad7: Download complete\n9333b8d7b119: Verifying Checksum\n9333b8d7b119: Download complete\ne4d6e1f8f7b0: Verifying Checksum\ne4d6e1f8f7b0: Download complete\nde906d5248f0: Verifying Checksum\nde906d5248f0: Download complete\nd8d1b9d0fad7: Pull complete\nff8923c0c81d: Pull complete\na0e4bf411830: Pull complete\nfe23b5934555: Pull complete\n9cbeb98e2f73: Pull complete\ne4d6e1f8f7b0: Pull complete\n184ea3f39f9e: Verifying Checksum\n184ea3f39f9e: Download complete\n",
    "stdout": ""
  },
  "state": "RUNNING",
  "task_logs": null
}

```

It is running! Wait for seconds, and again:

```curl=
$ curl -s localhost:1122/runs/98a99495-2a3a-40ce-b033-46ad01ab0044 | jq .
{
  "outputs": [
    {
      "file_name": "SRR1274307_1.fastq.gz",
      "file_url": "http://localhost:1122/runs/98a99495-2a3a-40ce-b033-46ad01ab0044/data/outputs/SRR1274307_1.fastq.gz"
    },
    {
      "file_name": "SRR1274307_2.fastq.gz",
      "file_url": "http://localhost:1122/runs/98a99495-2a3a-40ce-b033-46ad01ab0044/data/outputs/SRR1274307_2.fastq.gz"
    }
  ],
  "request": {
    "tags": "{}\n",
    "workflow_attachment": [],
    "workflow_engine_name": "cwltool",
    "workflow_engine_parameters": "{}\n",
    "workflow_name": "download-fastq.cwl",
    "workflow_params": "{\n  \"run_ids\": [\n    \"SRR1274307\"\n  ],\n  \"repo\": \"ebi\",\n  \"nthreads\": 4\n}\n",
    "workflow_type": "CWL",
    "workflow_type_version": "v1.0",
    "workflow_url": "https://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl"
  },
  "run_id": "98a99495-2a3a-40ce-b033-46ad01ab0044",
  "run_log": {
    "cmd": "docker run -i --rm -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp -v /home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044:/home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044 -w=/home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/exe commonworkflowlanguage/cwltool:1.0.20191225192155 --outdir /home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/outputs https://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl /home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/exe/workflow_params.json 1>/home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/stdout.log 2>/home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/stderr.log",
    "end_time": "2021-03-11T22:21:16",
    "exit_code": 0,
    "name": "download-fastq.cwl",
    "start_time": "2021-03-11T22:19:53",
    "stderr": "\u001b[1;30mINFO\u001b[0m /usr/local/bin/cwltool 1.0.20191225192155\nCould not load extension schema https://schema.org/docs/schema_org_rdfa.html: None:11:92: Repeat node-elements inside property elements: http://www.w3.org/1999/xhtmlmeta\n\u001b[1;30mWARNING\u001b[0m \u001b[33mWorkflow checker warning:\nhttps://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl:14:5: Source 'nthreads'\n                                                                                                                         of type [\"null\",\n                                                                                                                         \"int\"] may be\n                                                                                                                         incompatible\nhttps://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl:41:7:   with sink\n                                                                                                                           'nthreads' of type\n                                                                                                                           \"int\"\nhttps://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl:19:5: Source 'repo' of\n                                                                                                                         type [\"null\",\n                                                                                                                         \"string\"] may be\n                                                                                                                         incompatible\nhttps://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl:33:7:   with sink 'repo'\n                                                                                                                           of type \"string\"\u001b[0m\n\u001b[1;30mINFO\u001b[0m [workflow ] start\n\u001b[1;30mINFO\u001b[0m [workflow ] starting step download_sra\n\u001b[1;30mINFO\u001b[0m [step download_sra] start\n\u001b[1;30mINFO\u001b[0m ['docker', 'pull', 'quay.io/inutano/download-sra:0.2.1']\n0.2.1: Pulling from inutano/download-sra\n5d20c808ce19: Pulling fs layer\n26033daab2b1: Pulling fs layer\n6936ed840dfa: Pulling fs layer\n5d20c808ce19: Download complete\n5d20c808ce19: Pull complete\n6936ed840dfa: Verifying Checksum\n6936ed840dfa: Download complete\n26033daab2b1: Verifying Checksum\n26033daab2b1: Download complete\n26033daab2b1: Pull complete\n6936ed840dfa: Pull complete\nDigest: sha256:69f1ca73377435be390bffede86219f3a5c4aa63aeb7b8041089a77a22d75027\nStatus: Downloaded newer image for quay.io/inutano/download-sra:0.2.1\n\u001b[1;30mINFO\u001b[0m [job download_sra] /tmp/1k8ba4u6$ docker \\\n    run \\\n    -i \\\n    --volume=/tmp/1k8ba4u6:/ebxWvx:rw \\\n    --volume=/tmp/pmjhk0_d:/tmp:rw \\\n    --workdir=/ebxWvx \\\n    --read-only=true \\\n    --user=0:0 \\\n    --rm \\\n    --env=TMPDIR=/tmp \\\n    --env=HOME=/ebxWvx \\\n    --cidfile=/tmp/uupe_aud/20210311222022-280547.cid \\\n    quay.io/inutano/download-sra:0.2.1 \\\n    download-sra \\\n    -r \\\n    ebi \\\n    SRR1274307\n--2021-03-11 22:20:23--  ftp://ftp.sra.ebi.ac.uk/vol1/srr/SRR127/007/SRR1274307\n           => 'SRR1274307.sra'\nResolving ftp.sra.ebi.ac.uk... 193.62.197.74\nConnecting to ftp.sra.ebi.ac.uk|193.62.197.74|:21... connected.\nLogging in as anonymous ... Logged in!\n==> SYST ... done.    ==> PWD ... done.\n==> TYPE I ... done.  ==> CWD (1) /vol1/srr/SRR127/007 ... done.\n==> SIZE SRR1274307 ... 946479\n==> PASV ... done.    ==> RETR SRR1274307 ... done.\nLength: 946479 (924K) (unauthoritative)\n\n     0K .......... .......... .......... .......... ..........  5% 80.8K 11s\n    50K .......... .......... .......... .......... .......... 10%  213K 7s\n   100K .......... .......... .......... .......... .......... 16% 30.5M 4s\n   150K .......... .......... .......... .......... .......... 21% 9.68M 3s\n   200K .......... .......... .......... .......... .......... 27%  219K 3s\n   250K .......... .......... .......... .......... .......... 32% 16.3M 2s\n   300K .......... .......... .......... .......... .......... 37% 11.2M 2s\n   350K .......... .......... .......... .......... .......... 43% 8.14M 1s\n   400K .......... .......... .......... .......... .......... 48%  227K 1s\n   450K .......... .......... .......... .......... .......... 54% 34.5M 1s\n   500K .......... .......... .......... .......... .......... 59% 40.9M 1s\n   550K .......... .......... .......... .......... .......... 64% 49.6M 1s\n   600K .......... .......... .......... .......... .......... 70% 36.6M 1s\n   650K .......... .......... .......... .......... .......... 75% 20.0M 0s\n   700K .......... .......... .......... .......... .......... 81% 16.2M 0s\n   750K .......... .......... .......... .......... .......... 86% 17.4M 0s\n   800K .......... .......... .......... .......... .......... 91%  226K 0s\n   850K .......... .......... .......... .......... .......... 97% 32.9M 0s\n   900K .......... .......... ....                            100% 11.9M=1.6s\n\n2021-03-11 22:20:29 (592 KB/s) - 'SRR1274307.sra' saved [946479]\n\n\u001b[1;30mINFO\u001b[0m [job download_sra] Max memory used: 1MiB\n\u001b[1;30mINFO\u001b[0m [job download_sra] completed success\n\u001b[1;30mINFO\u001b[0m [step download_sra] completed success\n\u001b[1;30mINFO\u001b[0m [workflow ] starting step pfastq_dump\n\u001b[1;30mINFO\u001b[0m [step pfastq_dump] start\n\u001b[1;30mINFO\u001b[0m ['docker', 'pull', 'quay.io/inutano/sra-toolkit:v2.9.0']\nv2.9.0: Pulling from inutano/sra-toolkit\nd8d1b9d0fad7: Pulling fs layer\nff8923c0c81d: Pulling fs layer\na0e4bf411830: Pulling fs layer\nfe23b5934555: Pulling fs layer\n9cbeb98e2f73: Pulling fs layer\ne4d6e1f8f7b0: Pulling fs layer\n184ea3f39f9e: Pulling fs layer\n9333b8d7b119: Pulling fs layer\nde906d5248f0: Pulling fs layer\nfe23b5934555: Waiting\n9cbeb98e2f73: Waiting\ne4d6e1f8f7b0: Waiting\n184ea3f39f9e: Waiting\n9333b8d7b119: Waiting\nde906d5248f0: Waiting\na0e4bf411830: Verifying Checksum\na0e4bf411830: Download complete\nff8923c0c81d: Verifying Checksum\nff8923c0c81d: Download complete\nfe23b5934555: Verifying Checksum\nfe23b5934555: Download complete\n9cbeb98e2f73: Verifying Checksum\n9cbeb98e2f73: Download complete\nd8d1b9d0fad7: Download complete\n9333b8d7b119: Verifying Checksum\n9333b8d7b119: Download complete\ne4d6e1f8f7b0: Verifying Checksum\ne4d6e1f8f7b0: Download complete\nde906d5248f0: Verifying Checksum\nde906d5248f0: Download complete\nd8d1b9d0fad7: Pull complete\nff8923c0c81d: Pull complete\na0e4bf411830: Pull complete\nfe23b5934555: Pull complete\n9cbeb98e2f73: Pull complete\ne4d6e1f8f7b0: Pull complete\n184ea3f39f9e: Verifying Checksum\n184ea3f39f9e: Download complete\n184ea3f39f9e: Pull complete\n9333b8d7b119: Pull complete\nde906d5248f0: Pull complete\nDigest: sha256:6fd4a55d66354ec14c363888fdc44ebac4531a263b00f799c810064cd6a591f2\nStatus: Downloaded newer image for quay.io/inutano/sra-toolkit:v2.9.0\n\u001b[1;30mINFO\u001b[0m [job pfastq_dump] /tmp/mpgxwo91$ docker \\\n    run \\\n    -i \\\n    --volume=/tmp/mpgxwo91:/ebxWvx:rw \\\n    --volume=/tmp/v6h32xdi:/tmp:rw \\\n    --volume=/tmp/1k8ba4u6/SRR1274307.sra:/var/lib/cwl/stgd9e1ef08-dfad-4dfb-aeaa-cbb2abf385c2/SRR1274307.sra:ro \\\n    --workdir=/ebxWvx \\\n    --read-only=true \\\n    --user=0:0 \\\n    --rm \\\n    --env=TMPDIR=/tmp \\\n    --env=HOME=/ebxWvx \\\n    --cidfile=/tmp/ykf3a62q/20210311222107-416357.cid \\\n    quay.io/inutano/sra-toolkit:v2.9.0 \\\n    pfastq-dump \\\n    --gzip \\\n    -t \\\n    4 \\\n    --readids \\\n    --skip-technical \\\n    --split-files \\\n    --split-spot \\\n    /var/lib/cwl/stgd9e1ef08-dfad-4dfb-aeaa-cbb2abf385c2/SRR1274307.sra\nUsing sra-stat : 2.9.0\nUsing fastq-dump : 2.9.0\ntmpdir: /ebxWvx\noutdir: /ebxWvx\nblocks: 1,6846 6847,13692 13693,20538 20539,27386\nRead 6846 spots for /var/lib/cwl/stgd9e1ef08-dfad-4dfb-aeaa-cbb2abf385c2/SRR1274307.sra\nWritten 6846 spots for /var/lib/cwl/stgd9e1ef08-dfad-4dfb-aeaa-cbb2abf385c2/SRR1274307.sra\nRead 6846 spots for /var/lib/cwl/stgd9e1ef08-dfad-4dfb-aeaa-cbb2abf385c2/SRR1274307.sra\nWritten 6846 spots for /var/lib/cwl/stgd9e1ef08-dfad-4dfb-aeaa-cbb2abf385c2/SRR1274307.sra\nRead 6846 spots for /var/lib/cwl/stgd9e1ef08-dfad-4dfb-aeaa-cbb2abf385c2/SRR1274307.sra\nWritten 6846 spots for /var/lib/cwl/stgd9e1ef08-dfad-4dfb-aeaa-cbb2abf385c2/SRR1274307.sra\nRead 6848 spots for /var/lib/cwl/stgd9e1ef08-dfad-4dfb-aeaa-cbb2abf385c2/SRR1274307.sra\nWritten 6848 spots for /var/lib/cwl/stgd9e1ef08-dfad-4dfb-aeaa-cbb2abf385c2/SRR1274307.sra\n\u001b[1;30mINFO\u001b[0m [job pfastq_dump] Max memory used: 0MiB\n\u001b[1;30mINFO\u001b[0m [job pfastq_dump] completed success\n\u001b[1;30mINFO\u001b[0m [step pfastq_dump] completed success\n\u001b[1;30mINFO\u001b[0m [workflow ] completed success\n\u001b[1;30mINFO\u001b[0m Final process status is success\n",
    "stdout": "{\n    \"fastq_files\": [\n        {\n            \"location\": \"file:///home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/outputs/SRR1274307_1.fastq.gz\",\n            \"basename\": \"SRR1274307_1.fastq.gz\",\n            \"class\": \"File\",\n            \"checksum\": \"sha1$22f01534b704d7024f36ce95cf975be80f4dda54\",\n            \"size\": 736698,\n            \"format\": \"http://edamontology.org/format_1930\",\n            \"path\": \"/home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/outputs/SRR1274307_1.fastq.gz\"\n        },\n        {\n            \"location\": \"file:///home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/outputs/SRR1274307_2.fastq.gz\",\n            \"basename\": \"SRR1274307_2.fastq.gz\",\n            \"class\": \"File\",\n            \"checksum\": \"sha1$c381b2fc6c3783716c5c0fe645a4df27b0006251\",\n            \"size\": 761425,\n            \"format\": \"http://edamontology.org/format_1930\",\n            \"path\": \"/home/ubuntu/git/github.com/ddbj/SAPPORO-service/run/98/98a99495-2a3a-40ce-b033-46ad01ab0044/outputs/SRR1274307_2.fastq.gz\"\n        }\n    ]\n}\n"
  },
  "state": "COMPLETE",
  "task_logs": null
}
```

The `state` turned to `"COMPLETE"`, now it's done! Sapporo-Service is hosting output files. Let's see if the output can actually be downloaded.

```shell=
$ curl -s localhost:1122/runs/98a99495-2a3a-40ce-b033-46ad01ab0044 | jq ".outputs"
[
  {
    "file_name": "SRR1274307_1.fastq.gz",
    "file_url": "http://localhost:1122/runs/98a99495-2a3a-40ce-b033-46ad01ab0044/data/outputs/SRR1274307_1.fastq.gz"
  },
  {
    "file_name": "SRR1274307_2.fastq.gz",
    "file_url": "http://localhost:1122/runs/98a99495-2a3a-40ce-b033-46ad01ab0044/data/outputs/SRR1274307_2.fastq.gz"
  }
]

$ curl -s localhost:1122/runs/98a99495-2a3a-40ce-b033-46ad01ab0044 | jq -r ".outputs[0].file_url" | xargs -I{} curl -s -O {}

$ ls ./SRR1274307_1.fastq.gz
./SRR1274307_1.fastq.gz
```

Woohoo! :tada: Now you successfully deployed your own CWL-as-a-Service!

## Sapporo-Web: A GUI for WES endpoint

Next we try to use Sapporo-Web, a web-based GUI application that allows users to run and manage workflows on a WES server. Sapporo-Web is implemented as a javascript SPA and hosted on GitHub Pages. You can access https://ddbj.github.io/SAPPORO-web/ or you can deploy your own Sapporo-Web (Recommend to use the Google Chrome browser). See details at https://github.com/ddbj/SAPPORO-web .

![](https://i.imgur.com/poWyOeM.png)

Here we use the one on GitHub pages. First, we need to register a WES endpoint we are going to use. Click the register button and input the address and the name for this endpoint. This time we input the localhost address `http://localhost:1122`, but make sure to use https protocol to avoid mixed content error if you try with your own server.

![](https://i.imgur.com/2QVuiJf.png)

If the server is successfully registered, the `service-info` will be shown up.

![](https://i.imgur.com/bILCnoG.png)

Next, we need to register a workflow to run on the server. Click register in the box of the workflow and input the URL we used above: `https://raw.githubusercontent.com/pitagora-network/pitagora-cwl/master/workflows/download-fastq/download-fastq.cwl`.

![](https://i.imgur.com/PHg47AG.png)

![](https://i.imgur.com/824gUSJ.jpg)

If the workflow is successfully registered, the workflow details and the form to input the parameters will appear.

![](https://i.imgur.com/otztTxo.jpg)

Here we input the same parameters we used.

![](https://i.imgur.com/RfxEE2C.png)

![](https://i.imgur.com/p2SlLvr.png)

Click the execute button to run the workflow.

![](https://i.imgur.com/yQ3buBc.png)

After a while, click the reload button next to the status badge.

![](https://i.imgur.com/RhFCeV0.png)

It's done again! You can download the output files.

![](https://i.imgur.com/qdX2sxv.png)

## Version history

- 1st version
  - https://github.com/ddbj/SAPPORO/blob/ca05ad2b9df62f9fb03f7444d90a86a8dfd16bce/docs/GettingStarted.md
- 2nd version
  - This document
