# coding: utf-8
import requests
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from requests.exceptions import RequestException


class CommonInfo(models.Model):
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        abstract = True


class Service(CommonInfo):
    name = models.CharField(_("Service name"), max_length=256, unique=True)
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
        api_server_url = self.api_server_url
        try:
            d_res = requests.get(
                "http://" + api_server_url + "/service-info").json()
        except RequestException:
            return False

        return d_res

    def insert_from_dict_response(self, d_res):
        self.save()
        for item in d_res["workflow_engines"]:
            workflow_engine = WorkflowEngine()
            workflow_engine.service = self
            workflow_engine.name = item["name"]
            workflow_engine.version = item["version"]
            workflow_engine.save()
            for item_2 in item["workflow_types"]:
                workflow_type = WorkflowType()
                workflow_type.workflow_engine = workflow_engine
                workflow_type.type = item_2["type"]
                workflow_type.version = item_2["version"]
                workflow_type.save()
        for val in d_res["supported_wes_versions"]:
            supported_wes_version = SupportedWesVersion()
            supported_wes_version.service = self
            supported_wes_version.wes_version = val
            supported_wes_version.save()
        for item in d_res["state_counts"]:
            state_count = StateCount()
            state_count.service = self
            state_count.state = item["state"]
            state_count.count = item["count"]
            state_count.save()
        self.auth_instructions_url = d_res["auth_instructions_url"]
        self.contact_info_url = d_res["contact_info_url"]

    def expand_to_dict(self):
        ret_dict = {
            "name": self.name,
            "api_server_url": self.api_server_url,
            "auth_instructions_url": self.auth_instructions_url,
            "contact_info_url": self.contact_info_url,
            "workflow_engines": [],
            "supported_wes_versions": [],
            "state_counts": [],
        }
        for workflow_engine in WorkflowEngine.objects.filter(service__id=self.id):
            d_engine = dict()
            d_engine["name"] = workflow_engine.name
            d_engine["version"] = workflow_engine.version
            d_engine["workflow_types"] = []
            for workflow_type in WorkflowType.objects.filter(workflow_engine__id=workflow_engine.id):
                d_workflow_type = dict()
                d_workflow_type["type"] = workflow_type.type
                d_workflow_type["version"] = workflow_type.version
                d_engine["workflow_types"].append(d_workflow_type)
            ret_dict["workflow_engines"].append(d_engine)
        for supported_wes_version in SupportedWesVersion.objects.filter(service__id=self.id):
            ret_dict["supported_wes_versions"].append(
                supported_wes_version.wes_version)
        for state_count in StateCount.objects.filter(service__id=self.id):
            d_state_count = dict()
            d_state_count["state"] = state_count.state
            d_state_count["count"] = state_count.count
            ret_dict["state_counts"].append(d_state_count)

        return ret_dict

    def get_workflows_dict_response(self):
        # Communication check with api server is validated in form
        api_server_url = self.api_server_url
        try:
            d_res = requests.get(
                "http://" + api_server_url + "/workflows").json()
        except RequestException:
            return False

        return d_res


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


class WorkflowType(CommonInfo):
    workflow_engine = models.ForeignKey(WorkflowEngine, verbose_name=_(
        "Belong workflow engine"), on_delete=models.CASCADE)
    type = models.CharField(_("Workflow type"), max_length=64)
    version = models.CharField(_("Workflow version"), max_length=64)

    class Meta:
        db_table = "workflow_type"
        verbose_name = "workflow_type"
        verbose_name_plural = "workflow_types"

    def __str__(self):
        return "Workflow Type: {} {}".format(self.type, self.version)


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


class StateCount(CommonInfo):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE)
    state = models.CharField(_("State"), max_length=64)
    count = models.IntegerField(_("Counte"))

    class Meta:
        db_table = "state_count"
        verbose_name = "state_count"
        verbose_name_plural = "state_counts"

    def __str__(self):
        return "State Count: {}, {}".format(self.state, str(self.count))
