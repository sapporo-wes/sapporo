# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from django.http import Http404

from app.models import Service, Workflow


class ServiceListView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        services = [service.expand_to_dict()
                    for service in Service.objects.all()]
        context = {
            "services": services,
        }

        return render(request, "app/service_list.html", context)


class ServiceDetailView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, service_name):
        service = Service.objects.filter(name=service_name).prefetch_related("workflows").prefetch_related(
            "workflow_engines__workflow_types").prefetch_related(
            "supported_wes_versions")
        if len(service) == 0:
            raise Http404
        context = {
            "service": service,
        }

        return render(request, "app/service_detail.html", context)
