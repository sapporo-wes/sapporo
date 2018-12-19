# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404

from app.models import Service


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
        service = get_object_or_404(Service, name=service_name)
        service = service.expand_to_dict()
        context = {
            "service": service,
        }
        return render(request, "app/service_detail.html", context)
