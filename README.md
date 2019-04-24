# SAPPORO

SAPPORO is a workflow and individual task execution system. It is also useful for continuous testing of workflows.

[Japanese document](https://hackmd.io/s/Syq0q0o8N)

![SAPPORO - Home](https://i.imgur.com/ebHAY8o.jpg)

## What does "individual task execution system" mean?

[Wikipedia - Batch Computing](https://en.wikipedia.org/wiki/Batch_processing)

> the scripted running of one or more programs, as directed by Job Control Language, with no human interaction other than, 

Batch computing is used in the following various areas.

- Machine learning
- Genome analysis
- Animation rendering
- Software testing
- Various simulations

These batch jobs can be ensured portability and reproducibility by using container technologies (e.g. Docker, Kubernetes, etc.), workflow execution engines (e.g. Airflow, Luigi, etc.) and workflow description languages (e.g. CWL, WDL, etc.).

![SAPPORO - Batch Job](https://i.imgur.com/4UJ799a.png)

## What does "useful for continuous testing of workflows" mean?

However, even if these technologies are used, since processing is executed on a physical computer, various practical problems occur.

- The server is shut down
- The network is shut down
- CPU resources, memory, storage, etc. are occupied by other processes
- A hosted container image is modified

In order to deal with these problems, in SAPPORO, the concept of CI/CD is introduced for the management of batch jobs. In other words, SAPPORO is intended to test if "the batch jobs are executing correctly" and "is the output of the batch job always the same (reproducible)".

## Features

- Verification of the reproducibility of a workflow
- Collect and manage batch job results
- Support for various workflow execution engines and workflow description languages
- Cooperation with various job schedulers
- Deployment to various environments (on-premise, cloud, cluster. etc.)
- docker-compose for simple deployment and management

## System Architecture

SAPPORO has two components: SAPPORO-web and SAPPORO-service.

- SAPPORO-web
  - User and batch job management interface
  - Web Server
- SAPPORO-service
  - Batch job executor
  - REST API Server

![SAPPORO - System Architecture](https://i.imgur.com/A4seI74.png)

You can register multiple SAPPORO-service in one SAPPORO-web or register one SAPPORO-service in multiple SAPPORO-web.

For details, please refer to each README.

- [SAPPORO-web - README](https://github.com/suecharo/SAPPORO/blob/master/SAPPORO-web/README.md)
- [SAPPORO-service - README](https://github.com/suecharo/SAPPORO/blob/master/SAPPORO-service/README.md)
- [SAPPORO-fileserver - README](https://github.com/suecharo/SAPPORO/blob/master/SAPPORO-fileserver/README.md)

## License

SAPPORO is released under the [Apache 2.0 license](https://github.com/suecharo/SAPPORO/blob/master/LICENSE).
