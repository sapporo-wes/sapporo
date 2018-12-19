# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DataListView(LoginRequiredMixin, TemplateView):
    template_name = "app/data_list.html"


class DataDetailView(LoginRequiredMixin, TemplateView):
    template_name = "app/data_detail.html"
