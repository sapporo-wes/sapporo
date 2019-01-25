# coding: utf-8
import requests
from pathlib import Path


RUN_ORDER_FILE_PATH = Path(__file__).resolve().parent.joinpath("bwa.yml")
URL = "http://localhost:8002/runs"


def post_runs():
    with RUN_ORDER_FILE_PATH.open(mode="rb") as f:
        data = {
            "workflow_name": "bwa_mapping_pe",
            "workflow_engine": "cwltool",
        }
        files = {
            "run_order": ("run_order.yml", f, "application/yaml;charset=UTF-8")
        }
        r = requests.post(URL, files=files, data=data)
    print(r.status_code)
    print(r.json())


if __name__ == "__main__":
    post_runs()
