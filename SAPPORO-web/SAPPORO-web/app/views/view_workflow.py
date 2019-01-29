# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from app.models import Workflow


class WorkflowListView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        workflows = Workflow.objects.all()
        context = {
            "workflows": workflows,
        }

        return render(request, "app/workflow_list.html", context)


class WorkflowDetailView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, workflow_token):
        workflow = get_object_or_404(Workflow, token=workflow_token)
        context = {
            "workflow": workflow,
        }

        return render(request, "app/workflow_detail.html", context)


class WorkflowPreparationView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, workflow_token):
        workflow = get_object_or_404(Workflow, token=workflow_token)
        context = {
            "workflow": workflow,
        }

        return render(request, "app/workflow_detail.html", context)
