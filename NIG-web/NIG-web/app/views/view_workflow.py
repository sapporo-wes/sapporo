# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class WorkflowListView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        return render(request, "app/workflow_list.html")


class WorkflowDetailView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, workflow_unique_id):
        return render(request, "app/workflow_detail.html")
