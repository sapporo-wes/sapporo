#!/bin/bash
# set -eux
set -eu

run_wf() {
  if [[ ${workflow_engine} == "cwltool" ]]; then
    run_cwltool
  elif [[ ${workflow_engine} == "nextflow" ]]; then
    run_nextflow
  elif [[ ${workflow_engine} == "toil" ]]; then
    run_toil
  fi
}

run_cwltool() {
  cwltool --outdir ${output_dir} ${workflow_file} ${run_order_file} 1> ${log_stdout_file} 2> ${log_stderr_file} || echo "EXECUTOR_ERROR" > ${state_file}
}

run_nextflow() {
  :
}

run_toil() {
  :
}

# =============

RUN_ORDER_FILE_NAME="run_order.yaml"
RUN_INFO_FILE_NAME="run_info.yaml"
STATE_FILE_NAME="state.txt"
LOG_STDOUT_FILE_NAME="stdout.log"
LOG_STDERR_FILE_NAME="stderr.log"

CMDNAME=$(basename $0)
if [[ $# -ne 1 ]]; then
  echo "Usage: $CMDNAME uuid" 1>&2
  exit 1
fi

uuid=$1
service_base_dir=$(cd $(dirname $0)/.. && pwd)
workflow_info_file=${service_base_dir}/workflow-info.yml
run_dir=${service_base_dir}/run/$(echo ${uuid} | cut -c 1-2)/${uuid}
output_dir=${run_dir}
run_order_file=${run_dir}/${RUN_ORDER_FILE_NAME}
run_info_file=${run_dir}/${RUN_INFO_FILE_NAME}
state_file=${run_dir}/${STATE_FILE_NAME}
log_stdout_file=${run_dir}/${LOG_STDOUT_FILE_NAME}
log_stderr_file=${run_dir}/${LOG_STDERR_FILE_NAME}
workflow_engine=$(cat ${run_info_file} | jq -r '.workflow_engine')
workflow_name=$(cat ${run_info_file} | jq -r '.workflow_name')
for i in $(seq 0 $(($(cat ${workflow_info_file} | yq '.workflows | length') - 1))); do
  name=$(cat ${workflow_info_file} | yq -r .workflows[$i].name)
  location=$(cat ${workflow_info_file} | yq -r .workflows[$i].location)
  if [[ ${name} == ${workflow_name} ]]; then
    if [[ $(echo ${location} | cut -c 1 ) == "/" ]]; then
      workflow_file=location
    else
      workflow_file=$(cd $(dirname ${service_base_dir}/${location}) && pwd)/$(basename ${location})
    fi
  fi
done

# TODO SIGKILL = cancel
trap 'echo "SYSTEM_ERROR" > ${state_file}' 1 2 3 9 15

echo "RUNNING" > ${state_file}

run_wf

echo "COMPLETE" > ${state_file}