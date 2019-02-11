# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from factory.django import DjangoModelFactory

from .model_service import CommonInfo, Service, WorkflowType


class Workflow(CommonInfo):
    service = models.ForeignKey(Service, verbose_name=_(
        "Service"), on_delete=models.CASCADE, related_name="workflows")
    name = models.CharField(_("Workflow name"), max_length=256)
    version = models.CharField(_("Workflow version"), max_length=256)
    workflow_type = models.ForeignKey(WorkflowType, verbose_name=_(
        "Workflow type"), on_delete=models.CASCADE, related_name="workflow")
    location = models.URLField(_("Workflow location"), max_length=256)
    content = models.TextField(_("Workflow content"))
    parameters_template_location = models.URLField(_(""), max_length=256)
    parameters_template = models.TextField(_("Workflow parameters template"))

    class Meta:
        db_table = "workflow"
        verbose_name = "workflow"
        verbose_name_plural = "workflows"

    def __str__(self):
        return "Workflow: {}".format(self.name)

    def find_excutable_engines(self):
        excutable_engines = []
        for workflow_engine in self.service.workflow_engines.all():
            for workflow_type in workflow_engine.workflow_types.all():
                if workflow_type.pk == self.workflow_type.pk:
                    excutable_engines.append(workflow_engine)

        return excutable_engines


class WorkflowFactory(DjangoModelFactory):
    class Meta:
        model = Workflow
