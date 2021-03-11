# SAPPORO

Sapporo is a workflow execution system (WES) that provides the [GA4GH WES Standard](https://github.com/ga4gh/workflow-execution-service-schemas) compatible API server and the Web GUI.

![SAPPORO - Home](https://i.imgur.com/ebHAY8o.jpg)

[Documentation in Japanese](https://hackmd.io/s/Syq0q0o8N)

## Features

- Easy to deploy with `docker-compose`
  - Suitable for on-premise, local cluster, cloud
- Workflow language and runner flexibility
  - A wrapper [`run.sh`](https://github.com/ddbj/SAPPORO-service/blob/master/sapporo/run.sh) encapsulates the differences in languages/runners/job schedulers

### Features work in progress

- Compatibility with object storage servers
- Collect and manage batch job results
- Verification of the reproducibility of a workflow

## Architecture

Sapporo has two components, Web and Service, which enable the cloud-friendly deployment. Sapporo-fileserver is also available for I/O testing.

- [SAPPORO-web](https://github.com/ddbj/SAPPORO-web)
  - Simple web application to providev graphical interface to manage users, jobs, and servers
- [SAPPORO-service](https://github.com/ddbj/SAPPORO-service)
  - An REST API implementation of [GA4GH WES](https://github.com/ga4gh/workflow-execution-service-schemas)
- [SAPPORO-fileserver](https://github.com/ddbj/SAPPORO-fileserver)
  - A tiny wrapper for [minio](https://minio.io) server for testing workflow input/output

![SAPPORO - System Architecture](https://i.imgur.com/A4seI74.png)

Users need to register Sapporo-service or other WES implementations to Sapporo-web to submit and manage workflows. Details of the components are in the documentation of each repository:

- [SAPPORO-web - README](https://github.com/ddbj/SAPPORO-web/blob/master/README.md)
- [SAPPORO-service - README](https://github.com/ddbj/SAPPORO-service/blob/master/README.md)
- [SAPPORO-fileserver - README](https://github.com/ddbj/SAPPORO-fileserver/blob/master/README.md)

## Aims and expectations

### Individual task execution system

From [Wikipedia - Batch Computing](https://en.wikipedia.org/wiki/Batch_processing):

> the scripted running of one or more programs, as directed by Job Control Language, with no human interaction other than,

Batch computing is a common technique used in the various fields of data engineering and science:

- Animation rendering
- Software testing
- Machine learning
- Genomic data analysis
- Simulations

Batch jobs usually have problems on portability and reproducibility, because many are implemented for a specific computing environment such as local computing clusters. Sapporo aims to support technologies such as container virtualization (e.g. Docker, Singularity, etc.), or workflow runners (e.g. Airflow, Luigi, etc.), and workflow languages ([Common Workflow Language](https://www.commonwl.org/), [Workflow Description Language](https://github.com/openwdl/wdl), [Nextflow](https://www.nextflow.io/), [Snakemake](https://snakemake.github.io/), etc.).

![SAPPORO - Batch Job](https://i.imgur.com/4UJ799a.png)

## Continuous testing of workflows

Packaging software in containers and describing processes in workflow languages are powerful methods to improve portability. However, there are still problems to prevent workflow execution like:

- Server down
- Network down
- Other processes occupies resources such as CPU, memory, or storage
- Unexpected modification of container images

Sapporo aims to introduce the continuous integration (CI) / continous deployment (CD) concept to the management of batch job execution. Testing batch job with WES can make sure that the registered batch job is running correctly, or failed at some point.

## License

SAPPORO is released under the [Apache 2.0 license](https://github.com/ddbj/SAPPORO/blob/master/LICENSE).
