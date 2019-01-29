# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from app.models import Workflow
from django.http import Http404
from app.forms import WorkflowPrepareForm
from app.lib.cwl_parser import parse_cwl_input_params


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
        workflow = Workflow.objects.filter(token=workflow_token).select_related("service", "workflow_type").first()
        excutable_engines = workflow.find_excutable_engines()
        input_params = parse_cwl_input_params(workflow.content)
        workflow_prepare_form = WorkflowPrepareForm(input_params, excutable_engines)

        return self.general_render(request, workflow, workflow_prepare_form)


    def post(self, request, workflow_token):
        workflow = Workflow.objects.filter(token=workflow_token).select_related("service", "workflow_type").first()
        excutable_engines = workflow.find_excutable_engines()
        input_params = parse_cwl_input_params(workflow.content)
        workflow_prepare_form = WorkflowPrepareForm(input_params, excutable_engines)

        return self.general_render(request, workflow, workflow_prepare_form)
    #     service_addition_form = ServiceAdditionForm()

    #     return self.general_render(request, service_addition_form)

    # def post(self, request, workflow_token):
    #     if request.POST.get("button_add_service"):
    #         service_addition_form = ServiceAdditionForm(request.POST)
    #         if service_addition_form.is_valid():
    #             service = Service()
    #             service.insert_from_form(
    #                 service_addition_form.cleaned_data["api_server_url"],
    #                 service_addition_form.cleaned_data["service_name"],
    #                 service_addition_form.cleaned_data["d_response"]
    #             )
    #             service.fetch_workflows()
    #     elif request.POST.get("button_delete_service"):
    #         for service_name in request.POST.getlist("delete_check"):
    #             service = Service.objects.get(name=service_name)
    #             service.delete()
    #         service_addition_form = ServiceAdditionForm()
    #     else:
    #         service_addition_form = ServiceAdditionForm()

    #     return self.general_render(request, service_addition_form)

    def general_render(self, request, workflow, workflow_prepare_form):
        context = {
            "workflow": workflow,
            "workflow_prepare_form": workflow_prepare_form,
        }

        return render(request, "app/workflow_prepare.html", context)
