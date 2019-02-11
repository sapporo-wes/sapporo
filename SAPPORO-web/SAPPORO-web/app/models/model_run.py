# coding: utf-8
from datetime import datetime

import requests
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from factory.django import DjangoModelFactory

from .model_service import CommonInfo, WorkflowEngine
from .model_workflow import Workflow


class Run(CommonInfo):
    user = models.ForeignKey(User, verbose_name=_(
        "Run Owner"), on_delete=models.CASCADE, related_name="runs")
    run_id = models.UUIDField(_("Run ID"))
    workflow = models.ForeignKey(Workflow, verbose_name=_(
        "Workflow"), on_delete=models.CASCADE, related_name="runs")
    execution_engine = models.ForeignKey(WorkflowEngine, verbose_name=_(
        "Workflow Engine"), on_delete=models.CASCADE, related_name="runs")
    workflow_parameters = models.TextField(_("Workflow parameters"))
    status = models.CharField(_("Status"), max_length=64)
    stdout = models.TextField(_("Run Stdout"), default="")
    stderr = models.TextField(_("Run Stderr"), default="")
    upload_url = models.URLField(_("Upload URL"), max_length=256, default="")
    start_time = models.DateTimeField(
        _("Start time"), auto_now=False, auto_now_add=False, null=True, blank=True)
    end_time = models.DateTimeField(
        _("End time"), auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        db_table = "run"
        verbose_name = "run"
        verbose_name_plural = "runs"

    def __str__(self):
        return "Run: {}".format(self.run_id)

    def _update_from_service(self):
        service_server_url = self.workflow.service.service_scheme + "://" + \
            self.workflow.service.service_host + "/runs/" + str(self.run_id)
        response = requests.get(service_server_url)
        assert response.status_code == 200, "Get run error"
        d_response = response.json()
        self.status = d_response["status"]
        self.stdout = d_response["stdout"]
        self.stderr = d_response["stderr"]
        self.upload_url = d_response["upload_url"]
        self.start_time = datetime.strptime(
            d_response["start_time"], "%Y-%m-%d %H:%M:%S")
        if d_response["end_time"] != "":
            self.end_time = datetime.strptime(
                d_response["end_time"], "%Y-%m-%d %H:%M:%S")
        self.save()


class RunFactory(DjangoModelFactory):
    class Meta:
        model = Run
