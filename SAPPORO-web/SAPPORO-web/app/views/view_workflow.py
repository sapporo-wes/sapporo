# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
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
        workflow = Workflow.objects.get(token=workflow_token)
        context = {
            "workflow": workflow,
        }

        return render(request, "app/workflow_detail.html", context)
