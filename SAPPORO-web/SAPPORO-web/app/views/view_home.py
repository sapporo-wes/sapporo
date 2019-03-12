# coding: utf-8
from logging import getLogger

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View

from app.forms import AuthenticationFormNoPlaceholder
from app.models import Run, Service, Workflow
from config.settings import ENABLE_USER_SIGNUP

logger = getLogger("django")


class HomeView(View):
    raise_exception = True

    def get(self, request):
        if settings.DEBUG:
            # for django.django-debug-toolbar
            logger.debug(request.META["REMOTE_ADDR"])

        if request.user.is_authenticated:
            services = Service.objects.all()
            workflows = Workflow.objects.all()
            runs = Run.get_user_recent_runs(request.user.pk)
            for run in runs:
                run.update_from_service()
            context = {
                "services": services,
                "workflows": workflows,
                "runs": runs,
            }
            return render(request, "app/home_authenticated.html", context)
        else:
            authentication_form = AuthenticationFormNoPlaceholder()
            context = {
                "authentication_form": authentication_form,
                "enable_user_signup": ENABLE_USER_SIGNUP,
            }
            return render(request, "app/home.html", context)

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request):
        if request.POST.get("authentication"):
            authentication_form = AuthenticationFormNoPlaceholder(
                request, data=request.POST)
            if authentication_form.is_valid():
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
                auth_login(request, authentication_form.get_user())
                return HttpResponseRedirect(redirect_to)
        else:
            authentication_form = AuthenticationFormNoPlaceholder(request)
        context = {
            "authentication_form": authentication_form,
        }

        return render(request, "app/home.html", context)
