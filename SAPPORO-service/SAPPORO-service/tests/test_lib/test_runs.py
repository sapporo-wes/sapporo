# coding: utf-8
import unittest
from pathlib import Path
from sys import path
from unittest.mock import MagicMock

from werkzeug.exceptions import BadRequest

try:
    base_dir = Path(__file__).resolve().parent.parent.parent
    path.append(str(base_dir))
except:
    pass


class TestRuns(unittest.TestCase):
    def setUp(self):
        from app.lib.util import read_workflow_info, read_service_info
        self.workflow_info = read_workflow_info()
        self.read_service_info = read_service_info()

    def test_execute(self):
        import app.lib.runs
        from app.lib.runs import execute
        app.lib.runs.prepare_run_dir = MagicMock()
        app.lib.runs.fork_run = MagicMock()
        parameters = {
            "workflow_name": self.workflow_info["workflows"][0]["name"],
            "workflow_engine": "cwltool",
            "run_order": "foo",
        }
        data = execute(parameters)
        self.assertIsInstance(data, dict)
        self.assertIn("run_id", data)

    def test_valudate_parameters_wrong_parameters(self):
        from app.lib.runs import validate_parameters
        parameters = {
            "workflow_name": self.workflow_info["workflows"][0]["name"],
            "workflow_engine": "cwltool",
        }
        self.assertRaises(BadRequest, lambda: validate_parameters(parameters))

    def test_confirm_exist_workflow_wrong_workflow(self):
        from app.lib.runs import confirm_exist_workflow
        self.assertRaises(
            BadRequest, lambda: confirm_exist_workflow("wrong_workflow"))

    def test_validate_engine_wrong_engine(self):
        from app.lib.runs import validate_engine
        self.assertRaises(
            BadRequest, lambda: validate_engine("cwltool", "wrong_type", "wrong_version"))
        self.assertRaises(
            BadRequest, lambda: validate_engine("wrong_engine", "wrong_type", "wrong_version"))
