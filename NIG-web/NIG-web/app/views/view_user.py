# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = "app/user_home.html"
