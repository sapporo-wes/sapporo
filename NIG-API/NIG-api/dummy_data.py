# coding: utf-8

DUMMY_SERVICE_INFO = {
    # The Workflow engine accepted by API-server and the Workflow definition accepted by that Workflow engine
    "workflow_type_versions": {
        "cwltool": {
            "workflow_type_version": [
                "CWL",
            ],
        },
    },
    "supported_wes_versions": [
        "1.0.0",
    ],
    "supported_filesystem_protocols": [
        "http",
        "https",
        "sftp",
        "s3",
        "file",
    ],
    "workflow_engine_versions": {
        "cwltool": "1.0.20181201184214",
    },
    # Default parameters accepted by the workflow engine
    "default_workflow_engine_parameters": [
        {
            "job_name": "string",
            "workflow_type": "string",
            "job_file": "string",
        },
    ],
    "system_state_counts": {
        "UNKNOWN": 0,
        "QUEUED": 0,
        "INITIALIZING": 0,
        "RUNNING": 0,
        "PAUSED": 0,
        "COMPLETE": 0,
        "EXECUTOR_ERROR": 0,
        "SYSTEM_ERROR": 0,
        "CANCELED": 0,
        "CANCELING": 0,
    },
    "auth_instructions_url": "https://github.com/suecharo/NIG",
    "contact_info_url": "https://github.com/suecharo/NIG",
    # Arbitrary parameter set, I'm wondering whether to use this
    "tags": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string",
    },
}


DUMMY_RUNS_LIST = {
    "runs": [
        {
            "run_id": "string",
            "state": "UNKNOWN"
        }
    ],
    "next_page_token": "string"
}

DUMMY_RUNS_RUN = {
    "run_id": "string"
}

DUMMY_RUNS_INFO = {
    "run_id": "string",
    "request": {
        "workflow_params": {},
        "workflow_type": "string",
        "workflow_type_version": "string",
        "tags": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        },
        "workflow_engine_parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        },
        "workflow_url": "string"
    },
    "state": "UNKNOWN",
    "run_log": {
        "name": "string",
        "cmd": [
            "string"
        ],
        "start_time": "string",
        "end_time": "string",
        "stdout": "string",
        "stderr": "string",
        "exit_code": 0
    },
    "task_logs": [
        {
            "name": "string",
            "cmd": [
                "string"
            ],
            "start_time": "string",
            "end_time": "string",
            "stdout": "string",
            "stderr": "string",
            "exit_code": 0
        }
    ],
    "outputs": {}
}

DUMMY_RUNS_CANCEL = {
    "run_id": "string"
}


DUMMY_RUNS_STATUS = {
    "run_id": "string",
    "state": "UNKNOWN"
}
