# coding: utf-8
from copy import copy
from io import StringIO

import requests
import yaml
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from requests.exceptions import RequestException

from app.forms import WorkflowParametersUploadForm, WorkflowPrepareForm
from app.lib.cwl_parser import (change_cwl_url_to_cwl_viewer_url,
                                parse_cwl_input_params)
from app.lib.mixin import MyLoginRequiredMixin as LoginRequiredMixin
from app.models import Run, Workflow


class WorkflowListView(LoginRequiredMixin, View):
    def get(self, request):
        workflows = Workflow.objects.select_related(
            "service", "workflow_type").filter(deleted=False).order_by("-updated_at")
        context = {
            "workflows": workflows,
        }

        return render(request, "app/workflow_list.html", context)


class WorkflowDetailView(LoginRequiredMixin, View):
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
            context["cwl_workflow_graph"] = change_cwl_url_to_cwl_viewer_url(
                workflow.location)

        return render(request, "app/workflow_detail.html", context)


class WorkflowPrepareView(LoginRequiredMixin, View):
    def get(self, request, workflow_token):
        workflow = Workflow.objects.filter(token=workflow_token, deleted=False).select_related(
            "service", "workflow_type").first()
        if workflow is None:
            raise Http404
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
                run = self.post_run(
                    request.user, workflow, workflow_engine, workflow_prepare_form.cleaned_data, input_params)
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
                d_workflow_parameters = self.load_upload_parameter_file(workflow_parameters)
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

    def post_run(self, user, workflow, workflow_engine, form_inputs, input_params):
        workflow_parameters = self.generate_wokrflow_parameters_yaml(form_inputs, input_params)
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
        run = Run.objects.create(
            user=user,
            name=form_inputs["run_name"],
            run_id=d_response["run_id"],
            service=workflow.service,
            workflow=workflow,
            execution_engine=workflow_engine,
            workflow_parameters=workflow_parameters,
            status=d_response["status"],
        )

        return run

    def generate_wokrflow_parameters_yaml(self, form_inputs, input_params):
        workflow_parameters = dict()
        for input_param in input_params:
            if input_param["type"] in ["File", "Directory"]:
                workflow_parameters[input_param["label"]] = dict()
                workflow_parameters[input_param["label"]]["class"] = input_param["type"]
                workflow_parameters[input_param["label"]]["path"] = form_inputs[input_param["label"]]
            else:
                workflow_parameters[input_param["label"]] = form_inputs[input_param["label"]]
        workflow_parameters = yaml.dump(
            workflow_parameters, default_flow_style=False)

        return workflow_parameters

    def load_upload_parameter_file(self, workflow_parameters):
        d_workflow_parameters = dict()
        d_load_parameters = yaml.load(workflow_parameters)
        for key, value in d_load_parameters.items():
            if isinstance(value, dict):
                d_workflow_parameters[key] = value["path"]
            else:
                d_workflow_parameters[key] = value
        
        return d_workflow_parameters
