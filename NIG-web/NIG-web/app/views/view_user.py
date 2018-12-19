# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class UserHomeView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, user_name):
        return render(request, "app/user_home.html")
