# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class WorkflowListView(LoginRequiredMixin, TemplateView):
    template_name = "app/workflow_list.html"


class WorkflowDetailView(LoginRequiredMixin, TemplateView):
    template_name = "app/workflow_detail.html"
