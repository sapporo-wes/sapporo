# coding: utf-8
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import View

from app.forms import ServiceAdditionForm
from app.lib.mixin import MyLoginRequiredMixin as LoginRequiredMixin
from app.models import Service


class AdminHomeView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied

        return render(request, "app/admin_home.html")


class AdminServiceView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied
        service_addition_form = ServiceAdditionForm()

        return self.general_render(request, service_addition_form)

    def post(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied
        if request.POST.get("button_add_service"):
            service_addition_form = ServiceAdditionForm(request.POST)
            if service_addition_form.is_valid():
                service = Service()
                service.create_from_form(service_addition_form.cleaned_data)
                service.create_workflows_from_server()
        elif request.POST.get("button_delete_service"):
            for service_name in request.POST.getlist("delete_check"):
                service = Service.objects.get(name=service_name)
                service.delete()
            service_addition_form = ServiceAdditionForm()
        elif request.POST.get("button_update_service"):
            for service_name in request.POST.getlist("update_check"):
                service = Service.objects.get(name=service_name)
                service.update_from_server()
                service.update_workflows_from_server()
            service_addition_form = ServiceAdditionForm()
        else:
            service_addition_form = ServiceAdditionForm()

        return self.general_render(request, service_addition_form)

    def general_render(self, request, service_addition_form):
        services = Service.objects.all().prefetch_related(
            "workflow_engines").prefetch_related("workflows")
        context = {
            "services": services,
            "service_addition_form": service_addition_form,
        }
        return render(request, "app/admin_service.html", context)
