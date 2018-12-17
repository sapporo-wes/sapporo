# coding: utf-8
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import requests
from requests.exceptions import RequestException
import sys


class CommonInfo(models.Model):
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        abstract = True


class Service(CommonInfo):
    name = models.CharField(_("Service name"), max_length=256)
    api_server_url = models.CharField(_("API server url"), max_length=256)
    auth_instructions_url = models.CharField(
        _("Auth instructions url"), max_length=256)
    contact_info_url = models.CharField(_("Contact info url"), max_length=256)

    class Meta:
        db_table = "service"
        verbose_name = "service"
        verbose_name_plural = "services"

    def __str__(self):
        return "Service: {}".format(self.name)

    def get_dict_response(self):
        # Communication check with api server is validated in form
        try:
            api_server_url = self.api_server_url
        except AttributeError:
            return False
        try:
            d_res = requests.get("http://" + api_server_url + "/service-info").json()
        except RequestException:
            return False

        return d_res

    def insert_from_dict_response(self, d_res):
        self.save()
        for key, value in d_res["workflow_type_versions"].items():
            workflow_engine = WorkflowEngine()
            workflow_engine.service = self
            workflow_engine.name = key  # cwltool
            workflow_engine.version = d_res["workflow_engine_versions"][key]
            workflow_engine.save()
            for item in value["workflow_type_version"]:
                workflow_type_version = WorkflowTypeVersion()
                workflow_type_version.workflow_engine = workflow_engine
                workflow_type_version.type_version = item
                workflow_type_version.save()
        for item in d_res["supported_wes_versions"]:
            supported_wes_version = SupportedWesVersion()
            supported_wes_version.service = self
            supported_wes_version.wes_version = item
            supported_wes_version.save()
        for item in d_res["supported_filesystem_protocols"]:
            supported_filesystem_protocol = SupportedFilesystemProtocol()
            supported_filesystem_protocol.service = self
            supported_filesystem_protocol.name = item
            supported_filesystem_protocol.save()
        # for default_workflow_engine_parameter in d_res["default_workflow_engine_parameters"]:
        #     for key, value in default_workflow_engine_parameter.items():
        #         default_workflow_engine_parameter = DefaultWorkflowEngineParameter()
        #         default_workflow_engine_parameter.service = self
        #         default_workflow_engine_parameter.key = key
        #         default_workflow_engine_parameter.value = value
        #         default_workflow_engine_parameter.save()
        for key, value in d_res["system_state_counts"].items():
            system_state_count = SystemStateCount()
            system_state_count.service = self
            system_state_count.state = key
            system_state_count.count = int(value)
            system_state_count.save()
        self.auth_instructions_url = d_res["auth_instructions_url"]
        self.contact_info_url = d_res["contact_info_url"]


class WorkflowEngine(CommonInfo):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE)
    name = models.CharField(_("Workflow engine name"), max_length=64)
    version = models.CharField(_("Workflow engine version"), max_length=64)

    class Meta:
        db_table = "workflow_engine"
        verbose_name = "workflow_engine"
        verbose_name_plural = "workflow_engines"

    def __str__(self):
        return "Workflow Engine: {}".format(self.name)


class WorkflowTypeVersion(CommonInfo):
    workflow_engine = models.ForeignKey(WorkflowEngine, verbose_name=_(
        "Belong workflow engine"), on_delete=models.CASCADE)
    type_version = models.CharField(_("Workflow type version"), max_length=64)

    class Meta:
        db_table = "workflow_type_version"
        verbose_name = "workflow_type_version"
        verbose_name_plural = "workflow_type_versions"

    def __str__(self):
        return "Workflow Type Version: {}".format(self.type_version)


class SupportedWesVersion(CommonInfo):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE)
    wes_version = models.CharField(_("Wes version"), max_length=64)

    class Meta:
        db_table = "supported_wes_version"
        verbose_name = "supported_wes_version"
        verbose_name_plural = "supported_wes_versions"

    def __str__(self):
        return "Supported Wes Version: {}".format(self.wes_version)


class SupportedFilesystemProtocol(CommonInfo):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE)
    name = models.CharField(_("Filesystem Protocol name"), max_length=64)

    class Meta:
        db_table = "supported_filesystem_protocol"
        verbose_name = "supported_filesystem_protocol"
        verbose_name_plural = "supported_filesystem_protocols"

    def __str__(self):
        return "Supported Filesystem Protocol: {}".format(self.name)


# class DefaultWorkflowEngineParameter(CommonInfo):
#     service = models.ForeignKey(Service, verbose_name=_(
#         "Belong service"), on_delete=models.CASCADE)
#     key = models.CharField(_("Parameter key"), max_length=64)
#     value = models.CharField(_("Parameter value"), max_length=64)

#     class Meta:
#         db_table = "default_workflow_engine_parameter"
#         verbose_name = "default_workflow_engine_parameter"
#         verbose_name_plural = "default_workflow_engine_parameters"

#     def __str__(self):
#         return "Default Workflow Engine Parameter: {}, {}".format(self.key, self.value)


class SystemStateCount(CommonInfo):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE)
    state = models.CharField(_("System state"), max_length=64)
    count = models.IntegerField(_("Counte"))

    class Meta:
        db_table = "system_state_count"
        verbose_name = "system_state_count"
        verbose_name_plural = "system_state_counts"

    def __str__(self):
        return "System State Count: {}, {}".format(self.state, str(self.count))
