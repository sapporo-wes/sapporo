# coding: utf-8
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View

from app.lib.mixin import MyLoginRequiredMixin as LoginRequiredMixin
from app.models import Service


class ServiceListView(LoginRequiredMixin, View):
    def get(self, request):
        services = Service.objects.filter(deleted=False).order_by("-updated_at").prefetch_related(
            "workflow_engines", "workflows")
        context = {
            "services": services,
        }

        return render(request, "app/service_list.html", context)


class ServiceDetailView(LoginRequiredMixin, View):
    def get(self, request, service_name):
        service = Service.objects.filter(name=service_name).prefetch_related(
            "workflows", "workflow_engines__workflow_types", "supported_wes_versions").first()
        if service is None:
            raise Http404
        context = {
            "service": service,
        }

        return render(request, "app/service_detail.html", context)
