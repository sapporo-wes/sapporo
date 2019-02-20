# coding: utf-8
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View
from django.utils.decorators import method_decorator

class HomeView(View):
    raise_exception = True

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "app/home_authenticated.html")
        else:
            authentication_form = AuthenticationForm()
            authentication_form.fields["username"].widget.attrs["placeholder"] = ""
            authentication_form.fields["password"].widget.attrs["placeholder"] = ""
            context = {
                "authentication_form": authentication_form,
            }
            return render(request, "app/home.html", context)

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request):
        if request.POST.get("authentication"):
            authentication_form = AuthenticationForm(
                request, data=request.POST)
            if authentication_form.is_valid():
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
                auth_login(request, authentication_form.get_user())
                return HttpResponseRedirect(redirect_to)
        else:
            authentication_form = AuthenticationForm(request)
        authentication_form.fields["username"].widget.attrs["placeholder"] = ""
        authentication_form.fields["password"].widget.attrs["placeholder"] = ""
        context = {
            "authentication_form": authentication_form,
        }

        return render(request, "app/home.html", context)
