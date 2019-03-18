# coding: utf-8
import io

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from app.lib.mixin import MyLoginRequiredMixin as LoginRequiredMixin
from app.lib.requests_wrapper import post_requests_no_data
from app.models import Run


class RunListView(LoginRequiredMixin, View):
    def get(self, request):
        runs = Run.get_user_runs(request.user.pk)
        for run in runs:
            run.update_from_service()
        context = {
            "runs": runs,
        }

        return render(request, "app/run_list.html", context)


class RunDetailView(LoginRequiredMixin, View):
    def get(self, request, run_id):
        run = get_object_or_404(Run, run_id=run_id)
        if request.user.pk != run.user.pk:
            raise PermissionDenied
        run.update_from_service()
        context = {
            "run": run,
            "bool_cancel_button": True if run.status in ["QUEUED", "RUNNING"] else False,
        }

        return render(request, "app/run_detail.html", context)

    def post(self, request, run_id):
        run = get_object_or_404(Run, run_id=run_id)
        if request.user.pk != run.user.pk:
            raise PermissionDenied
        run.update_from_service()
        if request.POST.get("run_cancel_button"):
            post_requests_no_data(run.workflow.service.server_scheme, run.workflow.service.server_host,
                                  "/runs/" + str(run.run_id) + "/cancel", run.workflow.service.server_token)
            run.update_from_service()
        context = {
            "run": run,
            "bool_cancel_button": True if run.status in ["QUEUED", "RUNNING"] else False,
        }

        return render(request, "app/run_detail.html", context)


class RunDownloadView(LoginRequiredMixin, View):
    def get(self, request, run_id):
        run = get_object_or_404(Run, run_id=run_id)
        if request.user.pk != run.user.pk:
            raise PermissionDenied
        run.update_from_service()
        content = io.StringIO()
        content.write(run.workflow_parameters)
        response = HttpResponse(content.getvalue(), content_type="text/plain")
        response["Content-Disposition"] = "filename=workflow_parameters_{}.txt".format(
            run.run_id)

        return response
