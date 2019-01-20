#!/bin/bash
set -eux

run_wf() {
  if [[ "${workflow_engine}" == "cwltool" ]]; then
    run_cwltool
  elif [[ "${workflow_engine}" == "nextflow" ]]; then
    run_nextflow
  elif [[ "${workflow_engine}" == "toil" ]]; then
    run_toil
  fi
}

run_cwltool() {
  cwltool "${workflow_file_path}" "${run_order_file_path}" 1> ${log_stdout_file_path} 2> ${log_stderr_file_path} || echo "ERROR" > "${state_file_path}"
}

run_nextflow() {
  # hogehoge
}

run_toil() {
  # hogehoge
}

# =============

RUN_ORDER_FILE_NAME="run-order.json"
RUN_INFO_FILE_NAME="run-info.json"
STATE_FILE_NAME="state.txt"
LOG_STDOUT_FILE_NAME="log.out"
LOG_STDERR_FILE_NAME="log.err"

CMDNAME=$(basename $0)
if [[ "$#" -ne 1 ]]; then
  echo "Usage: $CMDNAME uuid" 1>&2
  exit 1
fi

uuid="$1"
run_base_dir_path=$(cd $(dirname $0) && pwd)
run_dir_path="${run_base_dir_path}/${uuid}"
run_order_file_path="${run_dir_path}/${RUN_ORDER_FILE_NAME}"
run_info_file_path="${run_dir_path}/${RUN_INFO_FILE_NAME}"
state_file_path="${run_dir_path}/${STATE_FILE_NAME}"
log_stdout_file_path="${run_dir_path}/${LOG_STDOUT_FILE_NAME}"
log_stderr_file_path="${run_dir_path}/${LOG_STDERR_FILE_NAME}"
workflow_dir_path="${run_base_dir_path%run}workflow/workflow"

workflow_name=$(cat ${run_info_file_path} | jq -r '.name')
workflow_engine=$(cat ${run_info_file_path} | jq -r '.engine')
workflow_type=$(cat ${run_info_file_path} | jq -r '.type')
workflow_version=$(cat ${run_info_file_path} | jq -r '.version')

if [[ ${workflow_type} == "CWL" ]]; then
  ext="cwl"
elif [[ ${workflow_type} == "WDL" ]]; then
  ext="wdl"
elif [[ ${workflow_type} == "Nextflow" ]]; then
  ext="nf"
else
  echo "ERROR" > "${state_file_path}"
fi

workflow_file_path="${workflow_dir_path}/${workflow_name}.${ext}"

if [[ ! -e ${workflow_file_path} ]]; then
  echo "ERROR" > "${state_file_path}"
fi

trap 'echo "ERROR" > "${state_file_path}"' 1 2 3 9 15

echo "START" > "${state_file_path}"

run_wf

echo "FINISH" > "${state_file_path}"