# coding: utf-8
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.forms import AuthenticationFormNoPlaceholder, UserCreationForm
from config.settings import ENABLE_USER_SIGNUP


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("app:signin")
    template_name = "app/signup.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["enable_user_signup"] = ENABLE_USER_SIGNUP

        return context


class LoginNoPlaceholderView(LoginView):
    form_class = AuthenticationFormNoPlaceholder

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["enable_user_signup"] = ENABLE_USER_SIGNUP

        return context
