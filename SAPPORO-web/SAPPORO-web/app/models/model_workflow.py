# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from factory.django import DjangoModelFactory

from .model_service import CommonInfo, Service


class Workflow(CommonInfo):
    service = models.ForeignKey(Service, verbose_name=_(
        "Service"), on_delete=models.CASCADE, related_name="workflows")
    name = models.CharField(_("Workflow name"), max_length=256)
    type = models.CharField(_("Workflow type"), max_length=64)
    version = models.CharField(_("Workflow version"), max_length=64)
    content = models.TextField(_("Workflow content"))

    class Meta:
        db_table = "workflow"
        verbose_name = "workflow"
        verbose_name_plural = "workflows"

    def __str__(self):
        return "Workflow: {}".format(self.name)


class WorkflowFactory(DjangoModelFactory):
    class Meta:
        model = Workflow
