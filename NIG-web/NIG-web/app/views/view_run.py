# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class RunListView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        return render(request, "app/run_list.html")


class RunDetailView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, run_unique_id):
        return render(request, "app/run_detail.html")
