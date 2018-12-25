# coding: utf-8
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from app.models import Service, WorkflowEngine, WorkflowType


class CommonInfo(models.Model):
    created_at = models.DateTimeField(_("Created date"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        abstract = True


class Workflow(CommonInfo):
    name = models.CharField(_("Workflow name"), max_length=256)
    id_in_service = models.IntegerField(_("ID in service"))
    service = models.ForeignKey(Service, verbose_name=_(
        "Service"), on_delete=models.CASCADE)
    engine = models.ForeignKey(WorkflowEngine, verbose_name=_(
        "Workflow Engine"), on_delete=models.CASCADE)
    workflow_type = models.ForeignKey(WorkflowType, verbose_name=_(
        "Workflow Engine"), on_delete=models.CASCADE)
    description = models.TextField(_("Workflow Description"))

    def insert_from_dict_response(self, service, d_res):
        self.name = d_res["name"]
        self.id_in_service = d_res["id"]
        self.service = service
        self.engine = WorkflowEngine.objects.filter(
            service__id=service.id).get(name=d_res["engine"])
        self.workflow_type = WorkflowType.objects.filter(
            workflow_engine__id=self.engine.id, type=d_res["type"], version=d_res["version"]).first()
        self.description = d_res["description"]
        self.save()
        for item in d_res["parameters"]:
            parameter = WorkflowParameter()
            parameter.workflow = self
            parameter.name = item["name"]
            parameter.type = item["type"]
            parameter.description = item["description"]
            parameter.save()

    def expand_to_dict(self):
        ret_dict = {
            "name": self.name,
            "id_in_service": self.id_in_service,
            "engine": self.engine.name,
            "type": self.workflow_type.type,
            "version": self.workflow_type.version,
            "description": self.description,
            "parameters": [],
        }
        for item in WorkflowParameter.objects.filter(workflow__id=self.id):
            d_param = dict()
            d_param["name"] = item.name
            d_param["type"] = item.type
            d_param["description"] = item.description
            ret_dict["parameters"].append(d_param)

        return ret_dict

    class Meta:
        db_table = "workflow"
        verbose_name = "workflow"
        verbose_name_plural = "workflows"

    def __str__(self):
        return "Workflow: {}".format(self.name)


class WorkflowParameter(CommonInfo):
    name = models.CharField(_("Parameter name"), max_length=256)
    workflow = models.ForeignKey(Workflow, verbose_name=_(
        "workflow"), on_delete=models.CASCADE)
    type = models.CharField(_("Parameter type"), max_length=64)
    description = models.TextField(_("Parameter description"))

    class Meta:
        db_table = "workflow_paramter"
        verbose_name = "workflow_paramter"
        verbose_name_plural = "workflow_paramters"

    def __str__(self):
        return "Workflow Paramter: {}".format(self.name)
