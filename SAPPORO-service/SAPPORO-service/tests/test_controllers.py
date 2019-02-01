# coding: utf-8
import io
import json
import unittest
from pathlib import Path
from sys import path
from copy import deepcopy
from unittest.mock import MagicMock

from werkzeug.exceptions import HTTPException

try:
    base_dir = Path(__file__).resolve().parent.parent
    path.append(str(base_dir))
except:
    pass


class TestControllers(unittest.TestCase):
    def setUp(self):
        from app import create_app
        from app.lib.util import read_workflow_info, read_service_info
        self.app = create_app().test_client()
        self.workflow_info = read_workflow_info()
        self.read_service_info = read_service_info()

    def test_get_service_info(self):
        response = self.app.get("/service-info")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("auth_instructions_url", data)
        self.assertIn("contact_info_url", data)
        self.assertIn("supported_wes_versions", data)
        self.assertIn("workflow_engines", data)
        self.assertNotEqual(0, len(data["workflow_engines"]))
        for workflow_engine in data["workflow_engines"]:
            self.assertIn("name", workflow_engine)
            self.assertIn("version", workflow_engine)
            self.assertIn("workflow_types", workflow_engine)
            self.assertNotEqual(0, len(workflow_engine["workflow_types"]))
            for workflow_type in workflow_engine["workflow_types"]:
                self.assertIn("type", workflow_type)
                self.assertIn("version", workflow_type)

    def test_get_workflows_list(self):
        response = self.app.get("/workflows")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("workflows", data)
        self.assertNotEqual(0, len(data["workflows"]))
        for workflow in data["workflows"]:
            self.assertIn("name", workflow)
            self.assertIn("version", workflow)
            self.assertIn("type", workflow)
            self.assertIn("content", workflow)

    def test_get_runs(self):
        response = self.app.get("/runs")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_post_runs_no_post_data(self):
        self.assertRaises(HTTPException, lambda: self.app.post("/runs"))

    def test_post_runs(self):
        import app.controllers
        copy_execute = deepcopy(app.controllers.execute)
        app.controllers.execute = MagicMock(
            return_value={
                "run_id": "cb934824-385d-46a2-b8bf-1204b9ac6d04"})
        post_data = {
            "workflow_name": self.workflow_info["workflows"][0]["name"],
            "workflow_engine": "cwltool",
            "run_order": (io.BytesIO(b"foo"), "run_order"),
        }
        response = self.app.post(
            "/runs", data=post_data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("run_id", data)
        self.assertEqual(
            "cb934824-385d-46a2-b8bf-1204b9ac6d04", data["run_id"])
        app.controllers.execute = copy_execute

    def test_get_runs_uuid_int_id(self):
        import app.controllers
        copy_get_run_info = deepcopy(app.controllers.get_run_info)
        app.controllers.get_run_info = MagicMock(return_value={"foo": "bar"})
        response = self.app.get("/runs/cb934824-385d-46a2-b8bf-1204b9ac6d04")
        self.assertEqual(response.status_code, 200)
        app.controllers.get_run_info = copy_get_run_info

    def test_post_runs_cancel(self):
        import app.controllers
        copy_cancel_run = deepcopy(app.controllers.cancel_run)
        app.controllers.cancel_run = MagicMock(
            return_value={
                "run_id": "cb934824-385d-46a2-b8bf-1204b9ac6d04"})
        response = self.app.post(
            "/runs/cb934824-385d-46a2-b8bf-1204b9ac6d04/cancel")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("run_id", data)
        self.assertEqual(
            "cb934824-385d-46a2-b8bf-1204b9ac6d04", data["run_id"])
        app.controllers.cancel_run = copy_cancel_run
