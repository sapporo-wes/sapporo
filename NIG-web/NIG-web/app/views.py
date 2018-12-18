# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View

from app.forms import ServiceAdditionForm, UserCreationForm
from app.models import Service


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "app/home_authenticated.html")
        else:
            return render(request, "app/home.html")


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('app:signin')
    template_name = 'app/signup.html'


class ServiceListView(LoginRequiredMixin, View):
    def get(self, request):
        return self.general_render(request)

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

        return self.general_render(request)

    def general_render(self, request):
        services = [service.expand_to_dict for service in Service.objects.all()]
        service_addition_form = ServiceAdditionForm()
        context = {
            "services": services,
            "service_addition_form": service_addition_form,
        }
        return render(request, "app/service_list.html", context)


class JobListView(LoginRequiredMixin, TemplateView):
    template_name = "app/job_list.html"


class DataListView(LoginRequiredMixin, TemplateView):
    template_name = "app/data_list.html"


class UserDetailView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, user_name):
        user = get_object_or_404(User, username=user_name)

        return render(request, "app/user_detail.html", {"user": user})
