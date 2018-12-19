# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, View

from app.forms import ServiceAdditionForm
from app.models import Service


class ServiceListView(LoginRequiredMixin, View):
    def get(self, request):
        service_addition_form = ServiceAdditionForm()
        return self.general_render(request, service_addition_form)

    def post(self, request):
        if request.POST.get("button_add_service"):
            service_addition_form = ServiceAdditionForm(request.POST)
            if service_addition_form.is_valid():
                service = Service()
                service.name = service_addition_form.cleaned_data["service_name"]
                service.api_server_url = service_addition_form.cleaned_data["api_server_url"]
                d_res = service.get_dict_response()
                service.insert_from_dict_response(d_res)
                service.save()
        else:
            service_addition_form = ServiceAdditionForm()

        return self.general_render(request, service_addition_form)

    def general_render(self, request, service_addition_form):
        services = [service.expand_to_dict for service in Service.objects.all()]
        context = {
            "services": services,
            "service_addition_form": service_addition_form,
        }
        return render(request, "app/service_list.html", context)


class ServiceDetailView(LoginRequiredMixin, TemplateView):
    template_name = "app/service_detail.html"
