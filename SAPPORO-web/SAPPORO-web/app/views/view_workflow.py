# coding: utf-8
import json
from copy import copy
from io import StringIO
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
import requests
import yaml
from app.forms import WorkflowPrepareForm
from app.lib.cwl_parser import parse_cwl_input_params
from app.models import RunFactory, Workflow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View


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

        return render(request, "app/workflow_detail.html", context)


class WorkflowPrepareView(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, workflow_token):
        workflow = Workflow.objects.filter(token=workflow_token).select_related(
            "service", "workflow_type").first()
        excutable_engines = workflow.find_excutable_engines()
        input_params = parse_cwl_input_params(workflow.content)
        workflow_prepare_form = WorkflowPrepareForm(
            input_params, excutable_engines)

        return self.general_render(request, workflow, workflow_prepare_form)

    def post(self, request, workflow_token):
        workflow = Workflow.objects.filter(token=workflow_token).select_related(
            "service", "workflow_type").first()
        excutable_engines = workflow.find_excutable_engines()
        input_params = parse_cwl_input_params(workflow.content)
        if request.POST.get("workflow_prepare_form"):
            workflow_prepare_form = WorkflowPrepareForm(
                input_params, excutable_engines, request.POST)
            if workflow_prepare_form.is_valid():
                workflow_engine = [engine for engine in excutable_engines if engine.token == workflow_prepare_form.cleaned_data["execution_engine"]][0]
                run = self._post_run(request.user, workflow, workflow_engine, workflow_prepare_form.cleaned_data)
                return HttpResponseRedirect(reverse_lazy("app:run_detail", kwargs={"run_id": run.run_id}))
        else:
            workflow_prepare_form = WorkflowPrepareForm(
                input_params, excutable_engines)

        return self.general_render(request, workflow, workflow_prepare_form)

    def general_render(self, request, workflow, workflow_prepare_form):
        context = {
            "workflow": workflow,
            "workflow_prepare_form": workflow_prepare_form,
        }

        return render(request, "app/workflow_prepare.html", context)

    def _post_run(self, user, workflow, workflow_engine, form_inputs):
        api_server_url = "http://" + workflow.service.api_server_url + "/runs"
        run_order = copy(form_inputs)
        del run_order["execution_engine"]
        run_order = yaml.dump(run_order, default_flow_style=False)
        data = {
            "workflow_name": workflow.name,
            "workflow_engine": workflow_engine.name,
        }
        files = {
            "run_order": ("run_order.yml", StringIO(run_order), "application/yaml;charset=UTF-8")
        }
        response = requests.post(api_server_url, files=files, data=data)
        assert response.status_code == 200, "Workflow post error"
        d_response = json.loads(response.text)
        run = RunFactory(
            user=user,
            run_id=d_response["run_id"],
            workflow=workflow,
            engine=workflow_engine,
            run_order=run_order,
        )

        return run
