#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
doc: Use fastq file as input and do trimming and quality check. Quality checks are done before trimming and after trimming.

inputs:
  fastq_url:
    type: string
    label: Download link of FastQ file from next generation sequencer
  nthreads:
    type: int?
    default: 2
    label: (optional) Number of cpu cores to be used

steps:
  download_fastq:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/curl.cwl
    in:
      download_url: fastq_url
      downloaded_file_name:
        default: fastq.fq
      stderr_log_file_name:
        default: curl_fastq_stderr.log
    out:
      - downloaded_file
      - stderr_log
  qc_fastq:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/fastqc.cwl
    in:
      nthreads: nthreads
      fastq: download_fastq/downloaded_file
      stdout_log_file_name:
        default: fastqc_fastq_stdout.log
      stderr_log_file_name:
        default: fastqc_fastq_stderr.log
    out:
      - qc_result
      - stdout_log
      - stderr_log
  trimming:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/trimmomatic_se.cwl
    in:
      nthreads: nthreads
      fastq: download_fastq/downloaded_file
      stdout_log_file_name:
        default: trimmomatic_stdout.log
      stderr_log_file_name:
        default: trimmomatic_stderr.log
    out:
      - trimed_fastq
      - stdout_log
      - stderr_log
  qc_trimed_fastq:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/fastqc.cwl
    in:
      nthreads: nthreads
      fastq: trimming/trimed_fastq
      stdout_log_file_name:
        default: fastqc_trimed_fastq_stdout.log
      stderr_log_file_name:
        default: fastqc_trimed_fastq_stderr.log
    out:
      - qc_result
      - stdout_log
      - stderr_log

outputs:
  fastq:
    type: File
    outputSource: download_fastq/downloaded_file
  curl_fastq_stderr:
    type: File
    outputSource: download_fastq/stderr_log
  qc_fastq_result:
    type: File
    outputSource: qc_fastq/qc_result
  qc_fastq_stdout_log:
    type: File
    outputSource: qc_fastq/stdout_log
  qc_fastq_stderr_log:
    type: File
    outputSource: qc_fastq/stderr_log
  trimed_fastq:
    type: File
    outputSource: trimming/trimed_fastq
  trimming_stdout_log:
    type: File
    outputSource: trimming/stdout_log
  trimming_stderr_log:
    type: File
    outputSource: trimming/stderr_log
  qc_trimed_fastq_result:
    type: File
    outputSource: qc_trimed_fastq/qc_result
  qc_trimed_fastq_stdout_log:
    type: File
    outputSource: qc_trimed_fastq/stdout_log
  qc_trimed_fastq_stderr_log:
    type: File
    outputSource: qc_trimed_fastq/stderr_log
