# coding: utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm as NativeUserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _
from app.models import Service

import requests
from requests.exceptions import RequestException


class UserCreationForm(NativeUserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    email = EmailField(label=_("Email address"),
                       required=True, help_text=_("Required."))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ServiceAdditionForm(forms.Form):
    service_name = forms.SlugField(label=_(
        "Service Name"), max_length=256, required=True, help_text=_("Required. Letters, digits and -/_ only."))
    api_server_url = forms.CharField(label=_(
        "API server url"), max_length=256, required=True, help_text=_("Required. e.g. localhost:8000"))

    def clean(self):
        super().clean()
        try:
            d_response = requests.get(
                "http://" + self.cleaned_data["api_server_url"] + "/service-info").json()
        except RequestException:
            raise forms.ValidationError("Please enter the correct URL.")
        if Service.objects.filter(name=self.cleaned_data["service_name"]).exists():
            raise forms.ValidationError(
                "A form with that name already exists.")
        self.cleaned_data["d_response"] = d_response
