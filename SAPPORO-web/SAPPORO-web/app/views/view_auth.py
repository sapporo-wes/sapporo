# coding: utf-8
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from app.forms import AuthenticationFormNoPlaceholder

from app.forms import UserCreationForm


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("app:signin")
    template_name = "app/signup.html"


class LoginNoPlaceholderView(LoginView):
    form_class = AuthenticationFormNoPlaceholder
