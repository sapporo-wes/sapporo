from datetime import datetime

from django.test import TestCase

from app.models import (Service, SupportedFilesystemProtocol,
                        SupportedWesVersion, SystemStateCount, WorkflowEngine,
                        WorkflowTypeVersion)

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

    def test_workflow_engine_entries(self):
        self.set_up_db()
        workflow_engines = WorkflowEngine.objects.filter(
            service__name="TestService")
        self.assertEqual(len(workflow_engines), len(
            DUMMY_SERVICE_INFO["workflow_type_versions"]))
        for key, value in DUMMY_SERVICE_INFO["workflow_type_versions"].items():
            workflow_engine = WorkflowEngine.objects.filter(
                service__name="TestService").get(name=key)
            self.assertEqual(workflow_engine.version,
                             DUMMY_SERVICE_INFO["workflow_engine_versions"][key])
            self.assertIsInstance(workflow_engine.created_at, datetime)
            self.assertIsInstance(workflow_engine.updated_at, datetime)

    def test_workflow_type_version_entries(self):
        self.set_up_db()
        workflow_engines = WorkflowEngine.objects.filter(
            service__name="TestService")
        for workflow_engine in workflow_engines:
            workflow_type_versions = WorkflowTypeVersion.objects.filter(
                workflow_engine__name=workflow_engine.name)
            self.assertEqual(len(workflow_type_versions), len(
                DUMMY_SERVICE_INFO["workflow_type_versions"][workflow_engine.name]["workflow_type_version"]))
            for workflow_type_version in workflow_type_versions:
                self.assertIn(workflow_type_version.type_version,
                              DUMMY_SERVICE_INFO["workflow_type_versions"][workflow_engine.name]["workflow_type_version"])
                self.assertIsInstance(
                    workflow_type_version.created_at, datetime)
                self.assertIsInstance(
                    workflow_type_version.updated_at, datetime)

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

    def test_supported_filesystem_protocol_entries(self):
        self.set_up_db()
        supported_filesystem_protocols = SupportedFilesystemProtocol.objects.filter(
            service__name="TestService")
        self.assertEqual(len(supported_filesystem_protocols), len(
            DUMMY_SERVICE_INFO["supported_filesystem_protocols"]))
        for supported_filesystem_protocol in supported_filesystem_protocols:
            self.assertIn(supported_filesystem_protocol.name,
                          DUMMY_SERVICE_INFO["supported_filesystem_protocols"])
            self.assertIsInstance(
                supported_filesystem_protocol.created_at, datetime)
            self.assertIsInstance(
                supported_filesystem_protocol.updated_at, datetime)

    # def test_default_workflow_engine_parameter_entries(self):
    #     pass

    def test_system_state_count_entries(self):
        self.set_up_db()
        system_state_counts = SystemStateCount.objects.filter(
            service__name="TestService")
        self.assertEqual(len(system_state_counts), len(
            DUMMY_SERVICE_INFO["system_state_counts"].items()))
        for system_state_count in system_state_counts:
            self.assertIn(system_state_count.state,
                          DUMMY_SERVICE_INFO["system_state_counts"])
            self.assertEqual(system_state_count.count,
                             DUMMY_SERVICE_INFO["system_state_counts"][system_state_count.state])
            self.assertIsInstance(system_state_count.created_at, datetime)
            self.assertIsInstance(system_state_count.updated_at, datetime)
