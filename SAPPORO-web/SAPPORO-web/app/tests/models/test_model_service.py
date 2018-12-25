# coding: utf-8
from datetime import datetime

from django.test import TestCase

from app.models import (Service, StateCount, SupportedWesVersion,
                        WorkflowEngine, WorkflowType)
from app.tests.mock_server.dummy_data import DUMMY_SERVICE_INFO


class ServiceModelTests(TestCase):
    def set_up_db(self):
        service = Service()
        service.name = "TestService"
        service.api_server_url = "localhost:9999"
        d_res = service.get_dict_response()
        service.insert_from_dict_response(d_res)
        service.save()

    def test_get_dict_response(self):
        service = Service()
        service.name = "TestService"
        service.api_server_url = "localhost:9999"
        d_res = service.get_dict_response()
        self.assertIsInstance(d_res, dict)

    def test_get_dict_response_error(self):
        service = Service()
        d_res = service.get_dict_response()
        self.assertFalse(d_res)

    def test_insert_from_dict_response(self):
        service = Service()
        service.name = "TestService"
        service.api_server_url = "localhost:9999"
        d_res = service.get_dict_response()
        service.insert_from_dict_response(d_res)
        res = service.save()
        self.assertIsNone(res)

    def test_service_entries(self):
        self.set_up_db()
        service = Service.objects.get(name="TestService")
        self.assertEqual(service.name, "TestService")
        self.assertEqual(service.api_server_url, "localhost:9999")
        self.assertEqual(service.auth_instructions_url,
                         DUMMY_SERVICE_INFO["auth_instructions_url"])
        self.assertEqual(service.contact_info_url,
                         DUMMY_SERVICE_INFO["contact_info_url"])
        self.assertIsInstance(service.created_at, datetime)
        self.assertIsInstance(service.updated_at, datetime)

    def test_expand_to_dict(self):
        self.set_up_db()
        service = Service.objects.get(name="TestService")
        d_service = service.expand_to_dict()
        self.assertEqual(d_service["name"], "TestService")
        self.assertEqual(d_service["api_server_url"], "localhost:9999")
        self.assertEqual(d_service["auth_instructions_url"],
                         DUMMY_SERVICE_INFO["auth_instructions_url"])
        self.assertEqual(d_service["contact_info_url"],
                         DUMMY_SERVICE_INFO["contact_info_url"])
        for workflow_engine in d_service["workflow_engines"]:
            self.assertIn(workflow_engine["name"], [
                          item["name"] for item in DUMMY_SERVICE_INFO["workflow_engines"]])
            self.assertIn(workflow_engine["version"], [
                          item["version"] for item in DUMMY_SERVICE_INFO["workflow_engines"]])
            for workflow_type in workflow_engine["workflow_types"]:
                self.assertIn(workflow_type["type"], [
                              item_2["type"] for item in DUMMY_SERVICE_INFO["workflow_engines"] for item_2 in item["workflow_types"]])
                self.assertIn(workflow_type["version"], [
                              item_2["version"] for item in DUMMY_SERVICE_INFO["workflow_engines"] for item_2 in item["workflow_types"]])
        for state_count in d_service["state_counts"]:
            self.assertIn(state_count["state"], [
                          item["state"] for item in DUMMY_SERVICE_INFO["state_counts"]])
            self.assertIn(state_count["count"], [
                          item["count"] for item in DUMMY_SERVICE_INFO["state_counts"]])

    def test_get_workflows_dict_response(self):
        service = Service()
        service.name = "TestService"
        service.api_server_url = "localhost:9999"
        d_res = service.get_workflows_dict_response()
        self.assertIsInstance(d_res, dict)

    def test_get_workflows_dict_response_error(self):
        service = Service()
        d_res = service.get_workflows_dict_response()
        self.assertFalse(d_res)

    def test_return_str(self):
        self.set_up_db()
        service = Service.objects.get(name="TestService")
        self.assertEqual(str(service), "Service: TestService")


class WorkflowEngineModelTests(TestCase):
    def set_up_db(self):
        service = Service()
        service.name = "TestService"
        service.api_server_url = "localhost:9999"
        d_res = service.get_dict_response()
        service.insert_from_dict_response(d_res)
        service.save()

    def test_workflow_engine_entries(self):
        self.set_up_db()
        workflow_engines = WorkflowEngine.objects.filter(
            service__name="TestService")
        self.assertEqual(len(workflow_engines), len(
            DUMMY_SERVICE_INFO["workflow_engines"]))

    def test_return_str(self):
        self.set_up_db()
        workflow_engines = WorkflowEngine.objects.filter(
            service__name="TestService")
        for workflow_engine in workflow_engines:
            self.assertIn("Workflow Engine:", str(workflow_engine))


class WorkflowTypeTests(TestCase):
    def set_up_db(self):
        service = Service()
        service.name = "TestService"
        service.api_server_url = "localhost:9999"
        d_res = service.get_dict_response()
        service.insert_from_dict_response(d_res)
        service.save()

    def test_return_str(self):
        self.set_up_db()
        workflow_engines = WorkflowEngine.objects.filter(
            service__name="TestService")
        for workflow_engine in workflow_engines:
            workflow_types = WorkflowType.objects.filter(
                workflow_engine__id=workflow_engine.id)
            for workflow_type in workflow_types:
                self.assertIn("Workflow Type:",
                              str(workflow_type))


class SupportedWesVersionModelTests(TestCase):
    def set_up_db(self):
        service = Service()
        service.name = "TestService"
        service.api_server_url = "localhost:9999"
        d_res = service.get_dict_response()
        service.insert_from_dict_response(d_res)
        service.save()

    def test_supported_wes_version_entries(self):
        self.set_up_db()
        supported_wes_versions = SupportedWesVersion.objects.filter(
            service__name="TestService")
        self.assertEqual(len(supported_wes_versions), len(
            DUMMY_SERVICE_INFO["supported_wes_versions"]))
        for supported_wes_version in supported_wes_versions:
            self.assertIn(supported_wes_version.wes_version,
                          DUMMY_SERVICE_INFO["supported_wes_versions"])
            self.assertIsInstance(supported_wes_version.created_at, datetime)
            self.assertIsInstance(supported_wes_version.updated_at, datetime)

    def test_return_str(self):
        self.set_up_db()
        supported_wes_versions = SupportedWesVersion.objects.filter(
            service__name="TestService")
        for supported_wes_version in supported_wes_versions:
            self.assertIn("Supported Wes Version:", str(supported_wes_version))


class StateCountTests(TestCase):
    def set_up_db(self):
        service = Service()
        service.name = "TestService"
        service.api_server_url = "localhost:9999"
        d_res = service.get_dict_response()
        service.insert_from_dict_response(d_res)
        service.save()

    def test_state_count_entries(self):
        self.set_up_db()
        state_counts = StateCount.objects.filter(
            service__name="TestService")
        self.assertEqual(len(state_counts), len(
            DUMMY_SERVICE_INFO["state_counts"]))
        for state_count in state_counts:
            self.assertIn(state_count.state,
                          [item["state"] for item in DUMMY_SERVICE_INFO["state_counts"]])
            self.assertIn(state_count.count,
                          [item["count"] for item in DUMMY_SERVICE_INFO["state_counts"]])
            self.assertIsInstance(state_count.created_at, datetime)
            self.assertIsInstance(state_count.updated_at, datetime)

    def test_return_str(self):
        self.set_up_db()
        state_counts = StateCount.objects.filter(
            service__name="TestService")
        for state_count in state_counts:
            self.assertIn("State Count:", str(state_count))
