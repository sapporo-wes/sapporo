# coding: utf-8
from secrets import token_hex

import requests
from django.db import models
from django.http import Http404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from factory.django import DjangoModelFactory
from requests.exceptions import RequestException

from app.lib.requests_wrapper import get_requests


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
    SCHEME_CHOICES = (
        ("http", "http"),
        ("https", "https"),
    )

    name = models.CharField(_("Service name"), max_length=256, unique=True)
    server_scheme = models.CharField(
        _("Server scheme"), max_length=16, choices=SCHEME_CHOICES, default="http")
    server_host = models.CharField(_("Server host"), max_length=256)
    server_token = models.CharField(
        _("Server token"), max_length=256, null=True, blank=True)
    auth_instructions_url = models.CharField(
        _("Auth instructions url"), max_length=256)
    contact_info_url = models.CharField(_("Contact info url"), max_length=256)

    class Meta:
        db_table = "service"
        verbose_name = "service"
        verbose_name_plural = "services"

    def __str__(self):
        return "Service: {}".format(self.name)

    def insert_from_form(self, service_name, server_scheme, server_host, server_token, d_response):
        self.name = service_name
        self.server_scheme = server_scheme
        self.server_host = server_host
        self.server_token = server_token
        self.auth_instructions_url = d_response["auth_instructions_url"]
        self.contact_info_url = d_response["contact_info_url"]
        self.save()
        for workflow_engine in d_response["workflow_engines"]:
            obj_workflow_engine = WorkflowEngineFactory(
                service=self,
                name=workflow_engine["engine_name"],
                version=workflow_engine["engine_version"],
            )
            for workflow_type in workflow_engine["workflow_types"]:
                workflow_type = WorkflowTypeFactory(
                    type=workflow_type["language_type"],
                    version=workflow_type["language_version"],
                )
                obj_workflow_engine.workflow_types.add(workflow_type)
            obj_workflow_engine.save()
        for wes_version in d_response["supported_wes_versions"]:
            SupportedWesVersionFactory(
                service=self,
                wes_version=wes_version,
            )

    def fetch_workflows(self):
        from app.models.model_workflow import Workflow, WorkflowFactory
        d_response = get_requests(
            self.server_scheme, self.server_host, "/workflows", self.server_token)
        if d_response:
            raise Http404
        for workflow in d_response["workflows"]:
            obj_workflow = Workflow.objects.filter(
                name=workflow["workflow_name"]).first()
            workflow_type = WorkflowType.objects.filter(
                type=workflow["language_type"], version=workflow["language_version"])
            if len(workflow_type) == 0:
                workflow_type = WorkflowTypeFactory(
                    type=workflow["language_type"],
                    version=workflow["language_version"],
                )
            else:
                workflow_type = workflow_type.first()
            if obj_workflow is not None:    # update
                obj_workflow.version = workflow["workflow_version"]
                obj_workflow.workflow_type = workflow_type
                obj_workflow.location = workflow["workflow_location"]
                obj_workflow.content = workflow["workflow_content"]
                obj_workflow.parameters_template_location = workflow[
                    "workflow_parameters_template_location"]
                obj_workflow.parameters_template = workflow["workflow_parameters_template"]
                obj_workflow.save()
            else:   # create
                WorkflowFactory(
                    service=self,
                    name=workflow["workflow_name"],
                    version=workflow["workflow_version"],
                    workflow_type=workflow_type,
                    location=workflow["workflow_location"],
                    content=workflow["workflow_content"],
                    parameters_template_location=workflow["workflow_parameters_template_location"],
                    parameters_template=workflow["workflow_parameters_template"],
                )


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service


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
