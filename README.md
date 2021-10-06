# Sapporo: an implementation of GA4GH WES standard

[![Apache License](https://img.shields.io/badge/license-Apache%202.0-orange.svg?style=flat&color=important)](http://www.apache.org/licenses/LICENSE-2.0)

<img src="https://raw.githubusercontent.com/sapporo-wes/sapporo/main/logo/sapporo-WES.svg" width="400" style="display: block; margin-left: auto; margin-right: auto; margin-top: 30px; margin-bottom: 30px;" alt="sapporo-WES logo">

Sapporo is an implementation of Workflow Execution Service (WES) or so-called Workflow-as-a-Service.

## Getting Started

A hands-on introduction of Sapporo is available here: [Sapporo - Getting Started](https://github.com/sapporo-wes/sapporo/blob/main/docs/GettingStarted.md)

This guides you to:

1. deploy the API server `sapporo-service` on your local computer
1. use `curl` command to request a workflow run from CUI
1. use the browser-based GUI `sapporo-web` to request a workflow run on your local `sapporo-service`

## How it works

Sapporo has two independent components, `sapporo-service`, and `sapporo-web`.

### sapporo-service

[GitHub - ddbj/sapporo-service](https://github.com/sapporo-wes/sapporo-service)

Sapporo-service is an implementation of the Global Alliance for Genomics and Health (GA4GH) [Workflow Execution Service API specification](https://ga4gh.github.io/workflow-execution-service-schemas/docs/). Sapporo-service is a lightweight API server that receives a request from users and runs a workflow via the workflow runner selected by the user.

### sapporo-web

[GitHub - ddbj/sapporo-web](https://github.com/sapporo-wes/sapporo-web)

Sapporo-web is a browser-based GUI to manage workflows that run on a WES server. To run a workflow, users do the following three steps, (1) Register a WES server to run workflows, (2) Register a workflow definition file, (3) input parameters. Sapporo-web fetches workflow definition files from publicly available URLs.

## Why do I need to use Sapporo?

[DNA Data Bank of Japan (DDBJ)](https://ddbj.nig.ac.jp) has maintained a shared computing cluster for over 10 years. The demand that we often asked by the users is to share the tools and the workflows among the other users with ease. Every user has, however, different preferences for programming languages to implement their tool, or workflow platform and languages to bundle their analysis pipelines, which causes barriers for others to reuse.

We design Sapporo as a top layer over the tools, the workflow languages, and the workflow runners to abstract the way to execute a workflow run. This allows users to reuse the resources without learning a new framework. One who usually writes [Common Workflow Language (CWL)](https://commonwl.org) does not need to learn [nextflow](https://nextflow.io) to run a workflow from the great public resource [nf-core](https://nf-co.re), or one who prefers [snakemake](https://snakemake.readthedocs.io/en/stable/index.html) does not need to learn how to run a CWL workflow to use a tool from [Common Workflow Library](https://github.com/common-workflow-library).

Another benefit from deploying Sapporo is liberation from `ssh` to a server: it should sound fantastic especially for admins of shared computing infrastructure. Users will need to prepare the tools and compose their workflow, then throw them to the server to run. It enables an abstraction of computing resources that encourages the hybrid use of on-premise and cloud computing.

## Acknowledgement

The development of sapporo is supported by [DDBJ](https://ddbj.nig.ac.jp). We thank the members of the two user groups, the [pitagora network](https://pitagora-network.org/) and the [workflow meetup Japan](https://workflow-meetup-jp.github.io/). This work is partially supported by the CREST program of the Japan Science and Technology Agency (grant No. JPMJCR1501) and JSPS KAKENHI Grant Numbers 20J22439.

## License

[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0). See the [LICENSE](https://github.com/sapporo-wes/sapporo-web/blob/main/LICENSE).

## Notice

Please note that this repository is participating in a study into sustainability
of open source projects. Data will be gathered about this repository for
approximately the next 12 months, starting from 2021-06-16.

Data collected will include number of contributors, number of PRs, time taken to
close/merge these PRs, and issues closed.

For more information, please visit
[our informational page](https://sustainable-open-science-and-software.github.io/) or download our [participant information sheet](https://sustainable-open-science-and-software.github.io/assets/PIS_sustainable_software.pdf).
