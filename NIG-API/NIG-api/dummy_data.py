# coding: utf-8

DUMMY_SERVICE_INFO = {
    "workflow_type_versions": {
        "additionalProp1": {
            "workflow_type_version": [
                "string"
            ]
        },
        "additionalProp2": {
            "workflow_type_version": [
                "string"
            ]
        },
        "additionalProp3": {
            "workflow_type_version": [
                "string"
            ]
        }
    },
    "supported_wes_versions": [
        "string"
    ],
    "supported_filesystem_protocols": [
        "string"
    ],
    "workflow_engine_versions": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string"
    },
    "default_workflow_engine_parameters": [
        {
            "name": "string",
            "type": "string",
            "default_value": "string"
        }
    ],
    "system_state_counts": {
        "additionalProp1": 0,
        "additionalProp2": 0,
        "additionalProp3": 0
    },
    "auth_instructions_url": "string",
    "contact_info_url": "string",
    "tags": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string"
    }
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
