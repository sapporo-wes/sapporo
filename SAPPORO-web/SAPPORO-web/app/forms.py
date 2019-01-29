# coding: utf-8
import requests
from app.models import Service
from django import forms
from django.contrib.auth.forms import \
    UserCreationForm as NativeUserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _
from requests.exceptions import RequestException
import yaml


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


class WorkflowPrepareForm(forms.Form):
    execution_engine = forms.ChoiceField(required=True)

    def __init__(self, input_params, excutable_engines):
        """
        input_params -> list
            {
                label: str
                type: str (boolean, int, float, string)
                    - int, long, double -> int
                    - string, File, Directoru -> string
                default: str, boolean, int, float, None
                doc: str or None
            }
        """
        super().__init__()
        for input_param in input_params:
            if input_param["type"] == "boolean":
                self.fields[input_param["label"]] = forms.BooleanField()
            elif input_param["type"] == "int":
                self.fields[input_param["label"]] = forms.IntegerField()
            elif input_param["type"] == "float":
                self.fields[input_param["label"]] = forms.FloatField()
            elif input_param["type"] == "string":
                self.fields[input_param["label"]] = forms.CharField()
            self.fields[input_param["label"]].required = True
            if input_param["default"] is not None:
                self.fields[input_param["label"]
                            ].initial = input_param["default"]
            if input_param["doc"] is not None:
                self.fields[input_param["label"]
                            ].help_text = input_param["doc"]
        self.fields["execution_engine"].choices = [
            [engine.token, engine.name] for engine in excutable_engines]
