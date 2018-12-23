# coding: utf-8
from django.test import TestCase

from app.models import Service, Workflow, WorkflowTool
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
            workflow = Workflow.objects.get(name=d_w["workflow_name"])
            self.assertEqual(workflow.id_in_service, d_w["workflow_id"])
            self.assertEqual(workflow.workflow_engine.name,
                             d_w["workflow_engine"])
            self.assertEqual(
                workflow.workflow_type_version.type_version, d_w["workflow_type_version"])
            self.assertEqual(workflow.description,
                             d_w["workflow_description"])
            self.assertIsNotNone(workflow.job_file_template)
            for workflow_tool in WorkflowTool.objects.filter(workflow__id=workflow.id):
                self.assertIn(workflow_tool.name, d_w["workflow_tools"])

    def test_expand_to_dict(self):
        self.set_up_db()
        workflows = Workflow.objects.all()
        for d_w in DUMMY_WORKFLOW_LIST["workflows"]:
            workflow = Workflow.objects.get(name=d_w["workflow_name"])
            d_workflow = workflow.expand_to_dict()

            self.assertEqual(d_workflow["name"], d_w["workflow_name"])
            self.assertEqual(d_workflow["id_in_service"], d_w["workflow_id"])
            self.assertEqual(
                d_workflow["workflow_engine"], d_w["workflow_engine"])
            self.assertEqual(
                d_workflow["workflow_type_version"], d_w["workflow_type_version"])
            self.assertEqual(d_workflow["description"],
                             d_w["workflow_description"])
            self.assertIsNotNone(d_workflow["job_file_template"])
            for workflow_tool in d_workflow["workflow_tools"]:
                self.assertIn(workflow_tool, d_w["workflow_tools"])
