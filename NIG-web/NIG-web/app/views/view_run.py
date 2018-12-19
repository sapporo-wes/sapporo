# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class RunListView(LoginRequiredMixin, TemplateView):
    template_name = "app/run_list.html"


class RunDetailView(LoginRequiredMixin, TemplateView):
    template_name = "app/run_detail.html"
