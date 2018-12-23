# coding: utf-8
DUMMY_SERVICE_INFO = {
    "workflow_engines": {
        {
            "name": "cwltool",
            "version": "1.0.20181201184214",
            "excutable_workflows": [
                {
                    "type": "CWL",
                    "version": "v1.0.2",
                },
                {
                    "type": "WDL",
                    "version": "0.0.5",
                },
            ],
        },
        {
            "name": "toil",
            "version": "3.18.0",
            "excutable_workflows": [
                {
                    "type": "CWL",
                    "version": "v1.0.2",
                },
            ],
        },
    },
    "state_counts": [
        {
            "state": "UNKNOWN",
            "count": 0
        },
        {
            "state": "INITIALIZING",
            "count": 0
        },
        {
            "state": "RUNNING",
            "count": 0
        },
        {
            "state": "COMPLETE",
            "count": 0
        },
        {
            "state": "ERROR",
            "count": 0
        },
    ],
    "supported_wes_versions": [
        "v1.0.0",
    ],
    "auth_instructions_url": "https://dummy_auth_instructions_url/",
    "contact_info_url": "https://dummy_contact_info_url/",
}

DUMMY_WORKFLOW_LIST = {
    "workflows": [
        {
            "id": 0,
            "name": "download-GRCh38",
            "engine": "cwltool",
            "type": "CWL",
            "version": "v1.0.2",
            "description": "Workflow for downloading fasta file and bwa index of GRCh38",
            "parameters": [
                {
                    "name": "key_1",
                    "description": "description_1",
                },
                {
                    "name": "key_2",
                    "description": "description_2",
                },
                {
                    "name": "key_3",
                    "description": "description_3",
                },
            ],
        },
        {
            "id": 1,
            "name": "test-workflow",
            "engine": "cwltool",
            "type": "CWL",
            "version": "v1.0.2",
            "description": "BWA mapping of paired end",
            "parameters": [
                {
                    "name": "key_1",
                    "description": "description_1",
                },
                {
                    "name": "key_2",
                    "description": "description_2",
                },
                {
                    "name": "key_3",
                    "description": "description_3",
                },
            ],
        },
        {
            "id": 2,
            "name": "test-workflow-from-SRA-Run-id",
            "engine": "cwltool",
            "type": "CWL",
            "version": "v1.0.2",
            "description": "BWA mapping of paired end",
            "parameters": [
                {
                    "name": "key_1",
                    "description": "description_1",
                },
                {
                    "name": "key_2",
                    "description": "description_2",
                },
                {
                    "name": "key_3",
                    "description": "description_3",
                },
            ],
        },
    ],
    "next_page_token": "dummy_next_page_token",
}

# TODO =======================================

# DUMMY_RUNS_LIST = {
#     "runs": [
#         {
#             "run_id": "0",
#             "state": "UNKNOWN",
#         },
#         {
#             "run_id": "1",
#             "state": "RUNNING",
#         },
#         {
#             "run_id": "2",
#             "state": "COMPLETE",
#         },
#         {
#             "run_id": "3",
#             "state": "CANCELED",
#         },
#     ],
#     # Optional
#     "next_page_token": "dummy_next_page_token",
# }

# DUMMY_RUNS_RUN = {
#     "run_id": "0",
# }

# DUMMY_RUNS_INFO = {
#     "run_id": "0",
#     "request": {
#         # Json
#         "workflow_params": {
#             "dummy_workflow_param_key_1": "dummy_workflow_param_value_1",
#             "dummy_workflow_param_key_2": "dummy_workflow_param_value_2",
#         },
#         # "workflow_type": "CWL",
#         "workflow_type_version": "string",
#         # "tags": {
#         #     "additionalProp1": "string",
#         #     "additionalProp2": "string",
#         #     "additionalProp3": "string"
#         # },
#         # "workflow_engine_parameters": {
#         #     "additionalProp1": "string",
#         #     "additionalProp2": "string",
#         #     "additionalProp3": "string"
#         # },
#         # "workflow_url": "dummy_workflow_url",
#         # TODO There is no Workflow Engine
#     },
#     "state": "UNKNOWN",
#     "run_log": {
#         "name": "dummy_run_name",
#         "cmd": [
#             "dummy_run_cmd_1",
#             "dummy_run_cmd_2",
#         ],
#         "start_time": "dummy_run_start_date",
#         "end_time": "dummy_run_end_date",
#         "stdout": "dummy_run_stdout",
#         "stderr": "dummy_run_stderr",
#         "exit_code": 0,
#     },
#     # "task_logs": [
#     #     {
#     #         "name": "dummy_task_1_name",
#     #         "cmd": [
#     #             "dummy_task_1_cmd_1",
#     #             "dummy_task_1_cmd_2",
#     #         ],
#     #         "start_time": "dummy_task_1_start_date",
#     #         "end_time": "dummy_task_1_end_date",
#     #         "stdout": "dummy_task_1_stdout",
#     #         "stderr": "dummy_task_1_stderr",
#     #         "exit_code": 0,
#     #     },
#     #     {
#     #         "name": "dummy_task_2_name",
#     #         "cmd": [
#     #             "dummy_task_2_cmd_1",
#     #             "dummy_task_2_cmd_2",
#     #         ],
#     #         "start_time": "dummy_task_2_start_date",
#     #         "end_time": "dummy_task_2_end_date",
#     #         "stdout": "dummy_task_2_stdout",
#     #         "stderr": "dummy_task_2_stderr",
#     #         "exit_code": 0,
#     #     },
#     # ],
#     # TODO
#     # "outputs": {}
# }

# DUMMY_RUNS_CANCEL = {
#     "run_id": "1",
# }


# DUMMY_RUNS_STATUS = {
#     "run_id": "1",
#     "state": "UNKNOWN",
# }
