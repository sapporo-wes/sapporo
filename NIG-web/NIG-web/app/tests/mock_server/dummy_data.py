# coding: utf-8

with open("./test_workflow_job_template.cwl") as f:
    test_workflow_job_template = f.read()
with open("./test_workflow_form_SRA_ID_job_template.cwl") as f:
    test_workflow_form_SRA_ID_job_template = f.read()

DUMMY_SERVICE_INFO = {
    # The Workflow engine accepted by API-server and the Workflow definition accepted by that Workflow engine
    # TODO Is there more than one version
    # TODO wrong form POST /runs
    "workflow_type_versions": {
        "cwltool": {
            "workflow_type_version": [
                "CWL v1.0.2",
                "WDL 0.0.5",
            ],
        },
        "toil": {
            "workflow_type_version": [
                "CWL v1.0.2",
            ],
        },
    },
    "supported_wes_versions": [
        "1.0.0",
        "0.2.0",
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
        "toil": "3.18.0",
    },
    # Default parameters accepted by the workflow engine
    # TODO The specification here is wrong. Entry for each engine is required.
    # "default_workflow_engine_parameters": [
    #     {
    #         "run_name": "string",
    #         "workflow_type": "string",
    #         "run_file": "string",
    #     },
    # ],
    "system_state_counts": {
        "UNKNOWN": 3,
        "QUEUED": 5,
        "INITIALIZING": 2,
        "RUNNING": 2,
        "PAUSED": 5,
        "COMPLETE": 1,
        "EXECUTOR_ERROR": 1,
        "SYSTEM_ERROR": 1,
        "CANCELED": 1,
        "CANCELING": 0,
    },
    "auth_instructions_url": "dummy_auth_instructions_url",
    "contact_info_url": "dummy_contact_info_url",
    # TODO Arbitrary parameter set, I'm wondering whether to use this
    # "tags": {
    #     "additionalProp1": "string",
    #     "additionalProp2": "string",
    #     "additionalProp3": "string",
    # },
}


DUMMY_RUNS_LIST = {
    "runs": [
        {
            "run_id": "0",
            "state": "UNKNOWN",
        },
        {
            "run_id": "1",
            "state": "RUNNING",
        },
        {
            "run_id": "2",
            "state": "COMPLETE",
        },
        {
            "run_id": "3",
            "state": "CANCELED",
        },
    ],
    # Optional
    "next_page_token": "dummy_next_page_token",
}

DUMMY_RUNS_RUN = {
    "run_id": "0",
}

DUMMY_RUNS_INFO = {
    "run_id": "0",
    "request": {
        # Json
        "workflow_params": {
            "dummy_workflow_param_key_1": "dummy_workflow_param_value_1",
            "dummy_workflow_param_key_2": "dummy_workflow_param_value_2",
        },
        # "workflow_type": "CWL",
        "workflow_type_version": "string",
        # "tags": {
        #     "additionalProp1": "string",
        #     "additionalProp2": "string",
        #     "additionalProp3": "string"
        # },
        # "workflow_engine_parameters": {
        #     "additionalProp1": "string",
        #     "additionalProp2": "string",
        #     "additionalProp3": "string"
        # },
        # "workflow_url": "dummy_workflow_url",
        # TODO There is no Workflow Engine
    },
    "state": "UNKNOWN",
    "run_log": {
        "name": "dummy_run_name",
        "cmd": [
            "dummy_run_cmd_1",
            "dummy_run_cmd_2",
        ],
        "start_time": "dummy_run_start_date",
        "end_time": "dummy_run_end_date",
        "stdout": "dummy_run_stdout",
        "stderr": "dummy_run_stderr",
        "exit_code": 0,
    },
    # "task_logs": [
    #     {
    #         "name": "dummy_task_1_name",
    #         "cmd": [
    #             "dummy_task_1_cmd_1",
    #             "dummy_task_1_cmd_2",
    #         ],
    #         "start_time": "dummy_task_1_start_date",
    #         "end_time": "dummy_task_1_end_date",
    #         "stdout": "dummy_task_1_stdout",
    #         "stderr": "dummy_task_1_stderr",
    #         "exit_code": 0,
    #     },
    #     {
    #         "name": "dummy_task_2_name",
    #         "cmd": [
    #             "dummy_task_2_cmd_1",
    #             "dummy_task_2_cmd_2",
    #         ],
    #         "start_time": "dummy_task_2_start_date",
    #         "end_time": "dummy_task_2_end_date",
    #         "stdout": "dummy_task_2_stdout",
    #         "stderr": "dummy_task_2_stderr",
    #         "exit_code": 0,
    #     },
    # ],
    # TODO
    # "outputs": {}
}

DUMMY_RUNS_CANCEL = {
    "run_id": "1",
}


DUMMY_RUNS_STATUS = {
    "run_id": "1",
    "state": "UNKNOWN",
}

# TODO our difinitions
DUMMY_WORKFLOW_LIST = {
    "workflows": [
        {
            "workflow_id": "0",
            "workflow_name": "download-GRCh38",
            "workflow_type_version": "CWL v1.0.2",
            "workflow_description": "Workflow for downloading fasta file and bwa index of GRCh38",
            "workflow_tools": [
                "download-GRCh38-fa.cwl",
                "download-GRCh38-alt.cwl",
                "bwa-index.cwl",
            ],
            "workflow_job_file_template": "",
        },
        {
            "workflow_id": "1",
            "workflow_name": "test-workflow",
            "workflow_type_version": "CWL v1.0.2",
            "workflow_description": "BWA mapping of paired end",
            "workflow_tools": [
                "fastqc.cwl",
                "trimmomaticPE.cwl",
                "bwa-mem-PE.cwl",
                "samtools-sam2bam.cwl",
                "picard-mark-duplicates.cwl",
                "picard-sort-sam.cwl",
            ],
            "workflow_job_file_template": test_workflow_job_template,
        },
        {
            "workflow_id": "2",
            "workflow_name": "test-workflow-from-SRA-Run-id",
            "workflow_type_version": "CWL v1.0.2",
            "workflow_description": "BWA mapping of paired end from SRA ID",
            "workflow_tools": [
                "download-sra.cwl",
                "pfastq-dump.cwl",
                "fastqc.cwl",
                "trimmomaticPE.cwl",
                "bwa-mem-PE.cwl",
                "samtools-sam2bam.cwl",
                "samtools-sort.cwl",
            ],
            "workflow_job_file_template": test_workflow_form_SRA_ID_job_template,
        },
    ],
    # Optional
    "next_page_token": "dummy_next_page_token",
}
