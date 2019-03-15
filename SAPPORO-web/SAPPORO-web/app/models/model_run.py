# coding: utf-8
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from app.lib.requests_wrapper import get_requests
from app.models.model_service import CommonInfo, Service, WorkflowEngine
from app.models.model_workflow import Workflow


class Run(CommonInfo):
    user = models.ForeignKey(User, verbose_name=_(
        "Run Owner"), on_delete=models.SET_NULL, related_name="runs", null=True, blank=True)
    name = models.CharField(_("Run Name"), max_length=256)
    run_id = models.UUIDField(_("Run ID"))
    service = models.ForeignKey(Service, verbose_name=_(
        "Service"), on_delete=models.SET_NULL, related_name="runs", null=True, blank=True)
    workflow = models.ForeignKey(Workflow, verbose_name=_(
        "Workflow"), on_delete=models.SET_NULL, related_name="runs", null=True, blank=True)
    execution_engine = models.ForeignKey(WorkflowEngine, verbose_name=_(
        "Workflow Engine"), on_delete=models.SET_NULL, related_name="runs", null=True, blank=True)
    workflow_parameters = models.TextField(_("Workflow parameters"))
    status = models.CharField(_("Status"), max_length=64)
    stdout = models.TextField(_("Run Stdout"), null=True, blank=True)
    stderr = models.TextField(_("Run Stderr"), null=True, blank=True)
    upload_url = models.URLField(
        _("Upload URL"), max_length=256, null=True, blank=True)
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

    def update_from_service(self):
        d_response = get_requests(self.service.server_scheme, self.service.server_host,
                                  "/runs/" + str(self.run_id), self.service.server_token)
        if d_response is None:
            raise Http404
        self.status = d_response["status"]
        self.stdout = d_response["stdout"]
        self.stderr = d_response["stderr"]
        self.upload_url = d_response["upload_url"]
        try:
            self.start_time = datetime.strptime(
                d_response["start_time"], "%Y-%m-%d %H:%M:%S")
        except:
            pass
        try:
            self.end_time = datetime.strptime(
                d_response["end_time"], "%Y-%m-%d %H:%M:%S")
        except:
            pass
        self.save()

    @classmethod
    def get_user_runs(cls, user_pk):
        return cls.objects.filter(user__pk=user_pk).order_by("-created_at")

    @classmethod
    def get_user_recent_runs(cls, user_pk):
        return cls.objects.filter(user__pk=user_pk).order_by("-created_at")[:10]
