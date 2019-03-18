# SAPPORO

SAPPORO is a job execution system for always reproducing Batch Job.

[Japanese document](https://hackmd.io/s/Syq0q0o8N)

![SAPPORO - Home](https://i.imgur.com/ebHAY8o.jpg)

## What does this mean always reproducing Batch Job

Batch computing is to run serial processing (called workflow, pipeline, etc.) on one or more computers without human operation. Batch computing is used in the following various areas.

- Machine learning
- Genome analysis
- Animation rendering
- Software testing
- Various simulations

These batch jobs can be ensured portability and reproducibility by using container technologies (e.g. Docker, Kubernetes, etc.), workflow execution engines (e.g. Airflow, Luigi, etc.) and workflow description languages (e.g. CWL, WDL, etc.).

![SAPPORO - Batch Job](https://i.imgur.com/4UJ799a.png)

However, even if these technologies are used, since processing is executed on a physical computer, various practical problems occur.

- Server is shut down
- Network is shut down
- CPU resources, memory, storage, etc. are occupied by other processes
- Hosted container image is modified

In order to deal with these problems, in SAPPORO, the concept of CI/CD is introduced to management of batch jobs. In other words, SAPPORO is intended to test wheter "batch jobs are always executable" and "output by batch job is always reproduced". SAPPORO aims to always reproduce batch jobs by introducing these concepts into the system.

## Feature

Features of SAPPORO are as follows.

- Verification of reproducibility of workflow
- Collect and manage batch job results
- Support for various workflow execution engines and workflow description languages
- Cooperation with various job schedulers
- Deployment to various envirounments(on-premise, cloud, cluster. etc.)
- Easy deployment and management

## System Architecture

SAPPORO divides into SAPPORO-web and SAPPORO-service.

- SAPPORO-web
  - Managing user informations and batch jobs
  - Web Server
  - Providing web frontend
- SAPPORO-service
  - Executing batch job
  - API Server
  - Providing REST API

![SAPPORO - System Architecture](https://i.imgur.com/A4seI74.png)

You can register multiple SAPPORO-service in one SAPPORO-web or register one SAPPORO-service in multiple SAPPORO-web.

For details, please refer to each README.

- [SAPPORO-web - README](https://github.com/suecharo/SAPPORO/blob/master/SAPPORO-web/README.md)
- [SAPPORO-service - README](https://github.com/suecharo/SAPPORO/blob/master/SAPPORO-service/README.md)

## License

SAPPORO is released under the [MIT license](https://github.com/suecharo/SAPPORO/blob/master/LICENSE).
