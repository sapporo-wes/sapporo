# coding: utf-8
import io

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from app.models import Run


class RunListView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        runs = Run.objects.filter(user__pk=request.user.pk)
        for run in runs:
            run._update_from_service()
        context = {
            "runs": runs,
        }

        return render(request, "app/run_list.html", context)


class RunDetailView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, run_id):
        run = get_object_or_404(Run, run_id=run_id)
        if request.user.pk != run.user.pk:
            raise PermissionDenied
        run._update_from_service()
        context = {
            "run": run,
        }

        return render(request, "app/run_detail.html", context)


class RunDownloadView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, run_id):
        run = get_object_or_404(Run, run_id=run_id)
        if request.user.pk != run.user.pk:
            raise PermissionDenied
        run._update_from_service()
        content = io.StringIO()
        content.write(run.workflow_parameters)
        response = HttpResponse(content.getvalue(), content_type="text/plain")
        response["Content-Disposition"] = "filename=workflow_parameters_{}.txt".format(
            run.run_id)

        return response
