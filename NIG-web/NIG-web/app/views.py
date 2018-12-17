# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View

from .forms import UserCreationForm


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


class ServiceListView(LoginRequiredMixin, TemplateView):
    template_name = "app/service_list.html"


class JobListView(LoginRequiredMixin, TemplateView):
    template_name = "app/job_list.html"


class DataListView(LoginRequiredMixin, TemplateView):
    template_name = "app/data_list.html"


class UserDetailView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, user_name):
        user = get_object_or_404(User, username=user_name)

        return render(request, "app/user_detail.html", {"user": user})
