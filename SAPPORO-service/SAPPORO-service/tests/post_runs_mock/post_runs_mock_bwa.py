# coding: utf-8
import requests
from pathlib import Path


WORKFLOW_PARAMETERS_FILE = Path(__file__).resolve().parent.joinpath("bwa.yml")
URL = "http://localhost:80/runs"


def post_runs():
    with WORKFLOW_PARAMETERS_FILE.open(mode="rb") as f:
        data = {
            "workflow_name": "bwa_mapping_pe",
            "execution_engine_name": "cwltool",
        }
        files = {
            "workflow_parameters": ("workflow_parameters.yml", f, "application/yaml;charset=UTF-8")
        }
        r = requests.post(URL, files=files, data=data)
    print(r.status_code)
    print(r.content)


if __name__ == "__main__":
    post_runs()
