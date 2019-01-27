# coding: utf-8
import unittest
from pathlib import Path
from sys import path

try:
    base_dir = Path(__file__).resolve().parent.parent.parent
    path.append(str(base_dir))
except:
    pass


class TestWorkflows(unittest.TestCase):
    def test_read_workflow_setting_file(self):
        from app.lib.workflows import read_workflow_setting_file
        data = read_workflow_setting_file()
        self.assertIn("workflows", data)

    def test_resolve_workflow_file_path(self):
        from app.lib.workflows import resolve_workflow_file_path
        test_cases = [
            ["/foo", False],
            ["/foo/bar/", False],
            ["/foo/baz.cwl", False],
            ["./foo/", False],
            ["./foo/baz.cwl", False],
            ["baz.cwl", False],
            ["./test_workflow/trimming_and_qc.cwl", True],
            ["./test_workflow", False],
        ]
        for location, result in test_cases:
            with self.subTest(location=location):
                if result:
                    path = resolve_workflow_file_path(location)
                    self.assertIsInstance(path, Path)
                else:
                    self.assertRaises(
                        AssertionError, lambda: resolve_workflow_file_path(location))
