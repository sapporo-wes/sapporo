#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
requirements:
  MultipleInputFeatureRequirement: {}
doc: BWA-mapping-PE is a mapping workflow using BWA for Peared-end reads. It receives two fastq files and one reference genome. Please enter download link of fastq files and reference genome. The reference genome will be indexed by BWA. Trimming, QC and bam sort will do too. QC result and sam / bam file will be output.

inputs:
  fastq1_url:
    type: string
    label: Download link of FastQ file from next generation sequencer
  fastq2_url:
    type: string
    label: Download link of FastQ file from next generation sequencer
  fasta_url:
    type: string
    label: Download link of Fasta file(e.g. GRCh38)
  nthreads:
    type: int?
    default: 2
    label: (optional) Number of cpu cores to be used
  aws_access_key_id:
    type: string
  aws_secret_access_key:
    type: string
  s3_bucket:
    type: string
  s3_upload_dir_name:
    type: string
    default: cwl_upload

steps:
  download_fastq1:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/curl.cwl
    in:
      download_url: fastq1_url
      downloaded_file_name:
        default: fastq1.fq
      stderr_log_file_name:
        default: curl_fastq1_stderr.log
    out:
      - downloaded_file
      - stderr_log
  download_fastq2:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/curl.cwl
    in:
      download_url: fastq2_url
      downloaded_file_name:
        default: fastq2.fq
      stderr_log_file_name:
        default: curl_fastq2_stderr.log
    out:
      - downloaded_file
      - stderr_log
  download_fasta:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/curl.cwl
    in:
      download_url: fasta_url
      downloaded_file_name:
        default: fasta.fa
      stderr_log_file_name:
        default: curl_fasta_stderr.log
    out:
      - downloaded_file
      - stderr_log
  qc_fastq1:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/fastqc.cwl
    in:
      nthreads: nthreads
      fastq: download_fastq1/downloaded_file
      stdout_log_file_name:
        default: fastqc_fastq1_stdout.log
      stderr_log_file_name:
        default: fastqc_fastq1_stderr.log
    out:
      - qc_result
      - stdout_log
      - stderr_log
  qc_fastq2:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/fastqc.cwl
    in:
      nthreads: nthreads
      fastq: download_fastq2/downloaded_file
      stdout_log_file_name:
        default: fastqc_fastq2_stdout.log
      stderr_log_file_name:
        default: fastqc_fastq2_stderr.log
    out:
      - qc_result
      - stdout_log
      - stderr_log
  trimming:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/trimmomatic_pe.cwl
    in:
      nthreads: nthreads
      fastq1: download_fastq1/downloaded_file
      fastq2: download_fastq2/downloaded_file
      stdout_log_file_name:
        default: trimmomatic_stdout.log
      stderr_log_file_name:
        default: trimmomatic_stderr.log
    out:
      - trimed_fastq1P
      - trimed_fastq1U
      - trimed_fastq2P
      - trimed_fastq2U
      - stdout_log
      - stderr_log
  qc_trimed_fastq1:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/fastqc.cwl
    in:
      nthreads: nthreads
      fastq: trimming/trimed_fastq1P
      stdout_log_file_name:
        default: fastqc_trimed_fastq1_stdout.log
      stderr_log_file_name:
        default: fastqc_trimed_fastq1_stderr.log
    out:
      - qc_result
      - stdout_log
      - stderr_log
  qc_trimed_fastq2:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/fastqc.cwl
    in:
      nthreads: nthreads
      fastq: trimming/trimed_fastq2P
      stdout_log_file_name:
        default: fastqc_trimed_fastq2_stdout.log
      stderr_log_file_name:
        default: fastqc_trimed_fastq2_stderr.log
    out:
      - qc_result
      - stdout_log
      - stderr_log
  bwa_index_build:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/bwa_index.cwl
    in:
      fasta: download_fasta/downloaded_file
      stdout_log_file_name:
        default: bwa_index_build_stdout.log
      stderr_log_file_name:
        default: bwa_index_build_stderr.log
    out:
      - amb
      - ann
      - bwt
      - pac
      - sa
      - stdout_log
      - stderr_log
  bwa_mapping:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/bwa_mem_pe.cwl
    in:
      nthreads: nthreads
      fasta: download_fasta/downloaded_file
      amb: bwa_index_build/amb
      ann: bwa_index_build/ann
      bwt: bwa_index_build/bwt
      pac: bwa_index_build/pac
      sa: bwa_index_build/sa
      fastq1: trimming/trimed_fastq1P
      fastq2: trimming/trimed_fastq2P
      stderr_log_file_name:
        default: bwa_mapping_stderr.log
    out:
      - sam
      - stderr_log
  sam2bam:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/samtools_sam2bam.cwl
    in:
      sam: bwa_mapping/sam
      stderr_log_file_name:
        default: samtools_sam2bam_stderr.log
    out:
      - bam
      - stderr_log
  mark_duplicates:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/picard_mark_duplicates.cwl
    in:
      bam: sam2bam/bam
      stdout_log_file_name:
        default: mark_duplicates_stdout.log
      stderr_log_file_name:
        default: mark_duplicates_stderr.log
    out:
      - marked_bam
      - metrix
      - stdout_log
      - stderr_log
  sort_bam:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/picard_sort_bam.cwl
    in:
      bam: mark_duplicates/marked_bam
      stdout_log_file_name:
        default: sort_bam_stdout.log
      stderr_log_file_name:
        default: sort_bam_stderr.log
    out:
      - sorted_bam
      - stdout_log
      - stderr_log
  s3_upload:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/s3_upload.cwl
    in:
      aws_access_key_id: aws_access_key_id
      aws_secret_access_key: aws_secret_access_key
      upload_file_list:
        source:
          - download_fastq1/downloaded_file
          - download_fastq1/stderr_log
          - download_fastq2/downloaded_file
          - download_fastq2/stderr_log
          - download_fasta/downloaded_file
          - download_fasta/stderr_log
          - qc_fastq1/qc_result
          - qc_fastq1/stdout_log
          - qc_fastq1/stderr_log
          - qc_fastq1/qc_result
          - qc_fastq1/stdout_log
          - qc_fastq1/stderr_log
          - trimming/trimed_fastq1P
          - trimming/trimed_fastq1U
          - trimming/trimed_fastq2P
          - trimming/trimed_fastq2U
          - trimming/stdout_log
          - trimming/stderr_log
          - qc_trimed_fastq1/qc_result
          - qc_trimed_fastq1/stdout_log
          - qc_trimed_fastq1/stderr_log
          - qc_trimed_fastq1/qc_result
          - qc_trimed_fastq1/stdout_log
          - qc_trimed_fastq1/stderr_log
          - bwa_index_build/amb
          - bwa_index_build/ann
          - bwa_index_build/bwt
          - bwa_index_build/pac
          - bwa_index_build/sa
          - bwa_index_build/stdout_log
          - bwa_index_build/stderr_log
          - bwa_mapping/sam
          - bwa_mapping/stderr_log
          - sam2bam/bam
          - sam2bam/stderr_log
          - mark_duplicates/marked_bam
          - mark_duplicates/metrix
          - mark_duplicates/stdout_log
          - mark_duplicates/stderr_log
          - sort_bam/sorted_bam
          - sort_bam/stdout_log
          - sort_bam/stderr_log
      s3_bucket: s3_bucket
      s3_upload_dir_name: s3_upload_dir_name
      stdout_log_file_name:
        default: s3_upload_stdout.log
      stderr_log_file_name:
        default: s3_upload_stderr.log
    out: []
  echo_s3_upload_url:
    run: https://github.com/suecharo/test-workflow/raw/master/tool/echo_s3_upload_url.cwl
    in:
      s3_bucket: s3_bucket
      s3_upload_dir_name: s3_upload_dir_name
      file_name:
        default: upload_url.txt
    out: [upload_url]

outputs:
  upload_url:
    type: File
    outputSource: echo_s3_upload_url/upload_url
