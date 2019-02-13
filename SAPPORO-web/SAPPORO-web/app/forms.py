# coding: utf-8
import requests
from django import forms
from django.contrib.auth.forms import \
    UserCreationForm as NativeUserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from requests.exceptions import RequestException

from app.models import Service


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
    SCHEME_CHOICES = (
        ("http", "http"),
        ("https", "https"),
    )

    service_name = forms.SlugField(label=_(
        "Service Name"), max_length=256, required=True, help_text=_("Required. Letters, digits and -/_ only."))
    server_scheme = forms.ChoiceField(
        choices=SCHEME_CHOICES, required=True, initial="http")
    server_host = forms.CharField(label=_(
        "Service server host"), max_length=256, required=True, help_text=_("Required. e.g. localhost:8000"))
    server_token = forms.CharField(label=_(
        "Service server token"), max_length=256, required=False, help_text=_("Not Required. None is OK."), initial="None")

    def clean(self):
        super().clean()
        try:
            d_response = requests.get(
                self.cleaned_data["server_scheme"] + "://" + self.cleaned_data["server_host"] + "/service-info").json()
        except RequestException:
            raise forms.ValidationError("Please enter the correct URL.")
        if Service.objects.filter(name=self.cleaned_data["service_name"]).exists():
            raise forms.ValidationError(
                "A form with that name already exists.")
        self.cleaned_data["d_response"] = d_response


class WorkflowPrepareForm(forms.Form):
    execution_engine = forms.ChoiceField(required=True)

    def __init__(self, workflow_name, input_params, excutable_engines, *args, **kwargs):
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
        super().__init__(*args, **kwargs)
        self.fields["run_name"] = forms.CharField(max_length=256, required=True, initial="{} {}".format(
            workflow_name, timezone.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.fields["execution_engine"].choices = [
            [engine.token, engine.name] for engine in excutable_engines]
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
