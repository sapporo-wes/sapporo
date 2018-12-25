# coding: utf-8
from django.test import TestCase

from app.models import Service, Workflow, WorkflowParameter
from app.tests.mock_server.dummy_data import DUMMY_WORKFLOW_LIST


class WorkflowModelTests(TestCase):
    def set_up_db(self):
        service = Service()
        service.name = "TestService"
        service.api_server_url = "localhost:9999"
        d_res = service.get_dict_response()
        service.insert_from_dict_response(d_res)
        service.save()
        l_workflow_d_res = service.get_workflows_dict_response()[
            "workflows"]
        for workflow_d_res in l_workflow_d_res:
            workflow = Workflow()
            workflow.insert_from_dict_response(service, workflow_d_res)
            workflow.save()

    def test_insert_from_dict_response(self):
        service = Service()
        service.name = "TestService"
        service.api_server_url = "localhost:9999"
        d_res = service.get_dict_response()
        service.insert_from_dict_response(d_res)
        service.save()
        l_workflow_d_res = service.get_workflows_dict_response()[
            "workflows"]
        for workflow_d_res in l_workflow_d_res:
            workflow = Workflow()
            workflow.insert_from_dict_response(service, workflow_d_res)
            res = workflow.save()
            self.assertIsNone(res)

    def test_workflow_entries(self):
        self.set_up_db()
        workflows = Workflow.objects.all()
        self.assertEqual(workflows.count(), len(
            DUMMY_WORKFLOW_LIST["workflows"]))
        for d_w in DUMMY_WORKFLOW_LIST["workflows"]:
            workflow = Workflow.objects.get(name=d_w["name"])
            self.assertEqual(workflow.id_in_service, d_w["id"])
            self.assertEqual(workflow.engine.name,
                             d_w["engine"])
            self.assertEqual(
                workflow.workflow_type.type, d_w["type"])
            self.assertEqual(
                workflow.workflow_type.version, d_w["version"])
            self.assertEqual(workflow.description,
                             d_w["description"])
            for workflow_parameter in WorkflowParameter.objects.filter(workflow__id=workflow.id):
                self.assertIn(workflow_parameter.name, [
                              item["name"] for item in d_w["parameters"]])
                self.assertIn(workflow_parameter.type, [
                              item["type"] for item in d_w["parameters"]])
                self.assertIn(workflow_parameter.description, [
                              item["description"] for item in d_w["parameters"]])

    def test_expand_to_dict(self):
        self.set_up_db()
        workflows = Workflow.objects.all()
        for d_w in DUMMY_WORKFLOW_LIST["workflows"]:
            workflow = Workflow.objects.get(name=d_w["name"])
            d_workflow = workflow.expand_to_dict()
            self.assertEqual(d_workflow["name"], d_w["name"])
            self.assertEqual(d_workflow["id_in_service"], d_w["id"])
            self.assertEqual(
                d_workflow["engine"], d_w["engine"])
            self.assertEqual(
                d_workflow["type"], d_w["type"])
            self.assertEqual(
                d_workflow["version"], d_w["version"])
            self.assertEqual(d_workflow["description"],
                             d_w["description"])
            for workflow_parameter in d_workflow["parameters"]:
                self.assertIn(workflow_parameter["name"], [
                              item["name"] for item in d_w["parameters"]])
                self.assertIn(workflow_parameter["type"], [
                              item["type"] for item in d_w["parameters"]])
                self.assertIn(workflow_parameter["description"], [
                              item["description"] for item in d_w["parameters"]])

    def test_return_str(self):
        self.set_up_db()
        for workflow in Workflow.objects.prefetch_related("workflowparameter_set").all():
            self.assertIn("Workflow:", str(workflow))
            for workflow_parameter in workflow.workflowparameter_set.all():
                self.assertIn("Workflow Paramter:", str(workflow_parameter))
