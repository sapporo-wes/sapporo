# SAPPORO

[![Apache License](https://img.shields.io/badge/license-Apache%202.0-orange.svg?style=flat&color=important)](http://www.apache.org/licenses/LICENSE-2.0)

<img src="https://raw.githubusercontent.com/ddbj/SAPPORO/master/logo/SAPPORO-WES.svg" width="400" style="display: block; margin-left: auto; margin-right: auto; margin-top: 30px; margin-bottom: 30px;" alt="SAPPORO-WES logo">

Sapporo is a standard implementation conforming to the Global Alliance for Genomics and Health (GA4GH) Workflow Execution Service (WES) API specification and a web application for managing and executing those WES services.

Sapporo has two components: **Sapporo-Service** is an API server which actually runs workflows via workflow runners, and **Sapporo-Web** is a browser-based GUI to manage the workflow execution running on WES servers.

**_GitHub Repository for each component_**

- [GitHub - ddbj/Sapporo-Service](https://github.com/ddbj/SAPPORO-service)
- [GitHub - ddbj/SSapporo-Web](https://github.com/ddbj/SAPPORO-web)

## Sapporo needs your help!

The [DDBJ](https://ddbj.nig.ac.jp) has maintained a shared computing cluster for over 10 years. The demand that we often asked by the users is to share the tools and the workflows among the other users with ease.

A year ago we made the first release of Sapporo. We have been dogfooding to investigate if the application suits our purpose. Now we published the major update, including the new features for both Sapporo-service and Sapporo-web. Sapporo-service is now a full implementation of the GA4GH WES standard, and ready for production deployment. Please try deploying Sapporo on your computer and run your workflows, and let us know what you think. Of course we welcome your pull request to [github/ddbj/Sapporo-service](https://github.com/ddbj/SAPPORO-service) or [github/ddbj/Sapporo-web](https://github/ddbj/Sapporo-web) !

## Acknowledgement

The development of Sapporo is supported by [DDBJ](https://ddbj.nig.ac.jp). We thank the members of the two user groups, the [pitagora network](https://pitagora-network.org/) and the [workflow meetup Japan](https://workflow-meetup-jp.github.io/). This work is partially supported by the CREST program of the Japan Science and Technology Agency (grant No. JPMJCR1501).

## License

[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0). See the [LICENSE](https://github.com/ddbj/SAPPORO-web/blob/master/LICENSE).
