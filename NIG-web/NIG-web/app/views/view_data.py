# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class DataListView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        return render(request, "app/data_list.html")


class DataDetailView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, data_unique_id):
        return render(request, "app/data_detail.html")
