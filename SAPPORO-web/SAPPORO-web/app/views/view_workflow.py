# coding: utf-8
from copy import copy
from io import StringIO

import requests
import yaml
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from requests.exceptions import RequestException

from app.forms import WorkflowParametersUploadForm, WorkflowPrepareForm
from app.lib.cwl_parser import parse_cwl_input_params
from app.models import RunFactory, Workflow
from app.lib.cwl_parser import change_cwl_url_to_cwl_viewer_url


class WorkflowListView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request):
        workflows = Workflow.objects.select_related(
            "service", "workflow_type").all()
        context = {
            "workflows": workflows,
        }

        return render(request, "app/workflow_list.html", context)


class WorkflowDetailView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, workflow_token):
        workflow = Workflow.objects.filter(
            token=workflow_token).select_related("service", "workflow_type").first()
        if workflow is None:
            raise Http404
        excutable_engines = workflow.find_excutable_engines()
        context = {
            "workflow": workflow,
            "excutable_engines": excutable_engines,
        }
        if workflow.workflow_type.type == "CWL":
            context["cwl_workflow_graph"] = change_cwl_url_to_cwl_viewer_url(workflow.location)

        return render(request, "app/workflow_detail.html", context)


class WorkflowPrepareView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, workflow_token):
        workflow = Workflow.objects.filter(token=workflow_token).select_related(
            "service", "workflow_type").first()
        excutable_engines = workflow.find_excutable_engines()
        input_params = parse_cwl_input_params(workflow.content)
        workflow_prepare_form = WorkflowPrepareForm(
            workflow.name, input_params, excutable_engines)
        workflow_parameters_upload_form = WorkflowParametersUploadForm()

        return self.general_render(request, workflow, workflow_prepare_form, workflow_parameters_upload_form)

    def post(self, request, workflow_token):
        workflow = Workflow.objects.filter(token=workflow_token).select_related(
            "service", "workflow_type").first()
        excutable_engines = workflow.find_excutable_engines()
        input_params = parse_cwl_input_params(workflow.content)
        if request.POST.get("workflow_prepare_form"):
            workflow_prepare_form = WorkflowPrepareForm(workflow.name,
                                                        input_params, excutable_engines, request.POST)
            if workflow_prepare_form.is_valid():
                workflow_engine = [engine for engine in excutable_engines if engine.token ==
                                   workflow_prepare_form.cleaned_data["execution_engine"]][0]
                run = self._post_run(
                    request.user, workflow, workflow_engine, workflow_prepare_form.cleaned_data)
                return HttpResponseRedirect(reverse_lazy("app:run_detail", kwargs={"run_id": run.run_id}))
            workflow_parameters_upload_form = WorkflowParametersUploadForm()
        elif request.POST.get("workflow_parameters_upload_form"):
            workflow_prepare_form = WorkflowPrepareForm(
                workflow.name, input_params, excutable_engines)
            workflow_parameters_upload_form = WorkflowParametersUploadForm(
                request.POST, request.FILES)
            if workflow_parameters_upload_form.is_valid():
                workflow_parameters = workflow_parameters_upload_form.cleaned_data["workflow_parameters"].file.read(
                ).decode("utf-8")
                d_workflow_parameters = yaml.load(workflow_parameters)
                for key, value in d_workflow_parameters.items():
                    workflow_prepare_form.fields[key].initial = value
        else:
            workflow_prepare_form = WorkflowPrepareForm(
                workflow.name, input_params, excutable_engines)
            workflow_parameters_upload_form = WorkflowParametersUploadForm()

        return self.general_render(request, workflow, workflow_prepare_form, workflow_parameters_upload_form)

    def general_render(self, request, workflow, workflow_prepare_form, workflow_parameters_upload_form):
        context = {
            "workflow": workflow,
            "workflow_prepare_form": workflow_prepare_form,
            "workflow_parameters_upload_form": workflow_parameters_upload_form,
        }

        return render(request, "app/workflow_prepare.html", context)

    def _post_run(self, user, workflow, workflow_engine, form_inputs):
        workflow_parameters = copy(form_inputs)
        del workflow_parameters["execution_engine"]
        del workflow_parameters["run_name"]
        workflow_parameters = yaml.dump(
            workflow_parameters, default_flow_style=False)
        data = {
            "workflow_name": workflow.name,
            "execution_engine_name": workflow_engine.name,
        }
        files = {
            "workflow_parameters": ("workflow_parameters.txt", StringIO(workflow_parameters), "text/plane;charset=UTF-8")
        }
        try:
            url = workflow.service.server_scheme + "://" + \
                workflow.service.server_host + "/runs"
            if workflow.service.server_token == "":
                response = requests.post(url, files=files, data=data)
            else:
                headers = {"Authorization": workflow.service.server_token}
                response = requests.post(
                    url, files=files, data=data, headers=headers)
            response.raise_for_status()
            d_response = response.json()
        except RequestException:
            raise Http404
        run = RunFactory(
            user=user,
            name=form_inputs["run_name"],
            run_id=d_response["run_id"],
            status=d_response["status"],
            workflow=workflow,
            execution_engine=workflow_engine,
            workflow_parameters=workflow_parameters,
        )

        return run
