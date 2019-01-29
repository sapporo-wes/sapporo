# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from app.models import Workflow
from django.http import Http404


class WorkflowListView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        workflows = Workflow.objects.select_related(
            "service", "workflow_type").all()
        context = {
            "workflows": workflows,
        }

        return render(request, "app/workflow_list.html", context)


class WorkflowDetailView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, workflow_token):
        workflow = Workflow.objects.filter(
            token=workflow_token).select_related("service", "workflow_type").first()
        if workflow is None:
            raise Http404
        excutable_engines = workflow.find_excutable_engines()
        context = {
            "workflow": workflow,
            "excutable_engines": excutable_engines,
        }

        return render(request, "app/workflow_detail.html", context)


class WorkflowPrepareView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, workflow_token):
        workflow = Workflow.objects.filter(
            token=workflow_token).select_related("service", "workflow_type").first()
        excutable_engines = workflow.find_excutable_engines()
        context = {
            "workflow": workflow,
            "excutable_engines": excutable_engines,
        }

        return render(request, "app/workflow_detail.html", context)
