# coding: utf-8
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from app.models import Service, WorkflowEngine, WorkflowTypeVersion


class CommonInfo(models.Model):
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        abstract = True


class Workflow(CommonInfo):
    name = models.CharField(_("Workflow name"), max_length=256)
    id_in_service = models.IntegerField(
        _("ID in service"), null=True, blank=True)
    service = models.ForeignKey(Service, verbose_name=_(
        "Service"), on_delete=models.CASCADE)
    workflow_engine = models.ForeignKey(WorkflowEngine, verbose_name=_(
        "Workflow Engine"), on_delete=models.CASCADE)
    workflow_type_version = models.ForeignKey(WorkflowTypeVersion, verbose_name=_(
        "Workflow Type Version"), on_delete=models.CASCADE)
    description = models.TextField(_("Workflow Description"))
    job_file_template = models.TextField(_("Job File Template"))

    def insert_from_dict_response(self, service, d_res):
        self.name = d_res["workflow_name"]
        self.id_in_service = d_res["workflow_id"]
        self.service = service
        self.workflow_engine = WorkflowEngine.objects.filter(service__id=service.id).get(
            name=d_res["workflow_engine"])
        self.workflow_type_version = WorkflowTypeVersion.objects.filter(workflow_engine__id=self.workflow_engine.id).get(
            type_version=d_res["workflow_type_version"])
        self.description = d_res["workflow_description"]
        self.workflow_job_file_template = d_res["workflow_job_file_template"]
        self.save()
        for item in d_res["workflow_tools"]:
            workflow_tool = WorkflowTool()
            workflow_tool.name = item
            workflow_tool.workflow = self
            workflow_tool.save()

    class Meta:
        db_table = "workflow"
        verbose_name = "workflow"
        verbose_name_plural = "workflows"

    def __str__(self):
        return "Workflow: {}".format(self.name)


class WorkflowTool(CommonInfo):
    name = models.CharField(_("Workflow tool name"), max_length=256)
    workflow = models.ForeignKey(Workflow, verbose_name=_(
        "workflow"), on_delete=models.CASCADE)

    class Meta:
        db_table = "workflow_tool"
        verbose_name = "workflow_tool"
        verbose_name_plural = "workflow_tools"

    def __str__(self):
        return "Workflow Tool: {}".format(self.name)
