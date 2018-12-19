# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AdminHomeView(LoginRequiredMixin, TemplateView):
    template_name = "app/admin_home.html"


class AdminServiceView(LoginRequiredMixin, TemplateView):
    template_name = "app/admin_service.html"
