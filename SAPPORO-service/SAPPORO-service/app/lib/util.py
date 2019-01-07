# coding: utf-8
from pathlib import Path

SERVICE_BASE_DIR = Path(__file__).absolute(
).parent.parent.parent.parent
WORKFLOW_BASE_DIR = SERVICE_BASE_DIR.joinpath("workflow")
