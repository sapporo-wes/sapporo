# coding: utf-8
from secrets import token_hex

import requests
from django.db import models
from django.http import Http404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from factory import LazyAttribute, fuzzy
from factory.django import DjangoModelFactory
from requests.exceptions import RequestException


def _get_token():
    # Cannot use lambda in Django model default
    return token_hex(16)


class CommonInfo(models.Model):
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)
    token = models.CharField(_("Token"), max_length=16,
                             unique=True, default=_get_token, primary_key=True)

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

    def insert_from_form(self, api_server_url, server_name, d_response):
        self.name = server_name
        self.api_server_url = api_server_url
        self.auth_instructions_url = d_response["auth_instructions_url"]
        self.contact_info_url = d_response["contact_info_url"]
        self.save()
        for workflow_engine in d_response["workflow_engines"]:
            obj_workflow_engine = WorkflowEngineFactory(
                service=self,
                name=workflow_engine["name"],
                version=workflow_engine["version"],
            )
            for workflow_type in workflow_engine["workflow_types"]:
                workflow_type = WorkflowTypeFactory(
                    type=workflow_type["type"],
                    version=workflow_type["version"],
                )
                obj_workflow_engine.workflow_types.add(workflow_type)
        for wes_version in d_response["supported_wes_versions"]:
            SupportedWesVersionFactory(
                service=self,
                wes_version=wes_version,
            )

    def fetch_workflows(self):
        # TODO update case
        from .model_workflow import WorkflowFactory
        try:
            d_response = requests.get(
                "http://" + self.api_server_url + "/workflows").json()
        except RequestException:
            raise Http404
        for workflow in d_response["workflows"]:
            workflow_type = WorkflowType.objects.filter(
                type=workflow["type"], version=workflow["version"])
            if len(workflow_type) == 0:
                workflow_type = WorkflowTypeFactory(
                    type=workflow["type"],
                    version=workflow["version"],
                )
            else:
                workflow_type = workflow_type.first()
            workflow = WorkflowFactory(
                service=self,
                name=workflow["name"],
                workflow_type=workflow_type,
                content=workflow["content"],
                job_template=workflow["job_template"]
            )


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service

    name = fuzzy.FuzzyText()
    api_server_url = LazyAttribute(
        lambda o: "{}_api_server_url@sapporo-example.com".format(o.name))
    auth_instructions_url = LazyAttribute(
        lambda o: "{}_auth_instructions_url@sapporo-example.com".format(o.name))
    contact_info_url = LazyAttribute(
        lambda o: "{}_contact_info_url@sapporo-example.com".format(o.name))


class WorkflowType(CommonInfo):
    type = models.CharField(_("Workflow type"), max_length=64)
    version = models.CharField(_("Workflow version"), max_length=64)

    class Meta:
        db_table = "workflow_type"
        verbose_name = "workflow_type"
        verbose_name_plural = "workflow_types"

    def __str__(self):
        return "Workflow Type: {} {}".format(self.type, self.version)


class WorkflowTypeFactory(DjangoModelFactory):
    class Meta:
        model = WorkflowType


class WorkflowEngine(CommonInfo):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE, related_name="workflow_engines")
    name = models.CharField(_("Workflow engine name"), max_length=64)
    version = models.CharField(_("Workflow engine version"), max_length=64)
    workflow_types = models.ManyToManyField(
        WorkflowType, verbose_name=_("Excutable workflow types"), related_name="workflow_engines")

    class Meta:
        db_table = "workflow_engine"
        verbose_name = "workflow_engine"
        verbose_name_plural = "workflow_engines"

    def __str__(self):
        return "Workflow Engine: {}".format(self.name)


class WorkflowEngineFactory(DjangoModelFactory):
    class Meta:
        model = WorkflowEngine


class SupportedWesVersion(CommonInfo):
    service = models.ForeignKey(Service, verbose_name=_(
        "Belong service"), on_delete=models.CASCADE, related_name="supported_wes_versions")
    wes_version = models.CharField(_("Wes version"), max_length=64)

    class Meta:
        db_table = "supported_wes_version"
        verbose_name = "supported_wes_version"
        verbose_name_plural = "supported_wes_versions"

    def __str__(self):
        return "Supported Wes Version: {}".format(self.wes_version)


class SupportedWesVersionFactory(DjangoModelFactory):
    class Meta:
        model = SupportedWesVersion
