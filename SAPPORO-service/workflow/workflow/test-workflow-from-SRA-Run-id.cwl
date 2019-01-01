#!/usr/bin/env cwl-runner

class: Workflow
id: test-workflow
label: test-workflow
cwlVersion: v1.0

$namespaces:
  edam: "http://edamontology.org/"

inputs:
  sra_run_ids:
    type: string[]
    doc: A list of SRA Run ID such as ERR034597

  download_repo:
    type: string?
    doc: (optional) The repository from which the data was downloaded (ncbi/ebi/ddbj). Default value is NCBI.

  nthreads:
    type: int
    doc: The number of cores to be used for parallel exec of fastq-dump

  fadir:
    type: Directory
    doc: directory containing FastA file and index for BWA aligner

  ref:
    type: string
    doc: name of reference (e.g., hs37d5) for BWA aligner

steps:
  download_sra:
    label: download_sra
    doc: Download .sra format sequence data from NCBI Sequence Read Archive
    run: ../tool/download-sra.cwl
    in:
      repo: download_repo
      run_ids: sra_run_ids
    out: [sraFiles]

  pfastq_dump:
    label: pfastq-dump
    doc: parallel execution of fastq-dump to convert .sra to .fastq.gz
    run: ../tool/pfastq-dump.cwl
    in:
      sraFiles: download_sra/sraFiles
      nthreads: nthreads
    out: [forward, reverse]

  qc1:
    label: qc1
    doc: Quality control for fastq file (fq1) before trimming
    run: ../tool/fastqc.cwl
    in:
      fastq: pfastq_dump/forward
      nthreads: nthreads
    out: [qc]

  qc2:
    label: qc2
    doc: Quality control for fastq file (fq2) before trimming
    run: ../tool/fastqc.cwl
    in:
      fastq: pfastq_dump/reverse
      nthreads: nthreads
    out: [qc]

  trimPE:
    label: trimPE
    doc: adaptor trimming
    run: ../tool/trimmomaticPE.cwl
    in:
      fq1: pfastq_dump/forward
      fq2: pfastq_dump/reverse
    out: [trimFq1P, trimFq2P]

  qc1P:
    label: qc1P
    doc: Quality control for fastq file (fq1) after trimming
    run: ../tool/fastqc.cwl
    in:
      fastq: trimPE/trimFq1P
      nthreads: nthreads
    out: [qc]

  qc2P:
    label: qc2P
    doc: Quality control for fastq file (fq2) after trimming
    run: ../tool/fastqc.cwl
    in:
      fastq: trimPE/trimFq2P
      nthreads: nthreads
    out: [qc]

  map:
    label: map
    doc: Mapping onto a reference genome
    run: ../tool/bwa-mem-PE.cwl
    in:
      fadir: fadir
      ref: ref
      fq1: trimPE/trimFq1P
      fq2: trimPE/trimFq2P
    out: [sam]

  sam2bam:
    label: sam2bam
    doc: Convert SAM to BAM
    run: ../tool/samtools-sam2bam.cwl
    in:
      sam: map/sam
    out: [bam]

  sort:
    label: sort
    doc: Sort BAM
    run: ../tool/samtools-sort.cwl
    in:
      bam: sam2bam/bam
    out: [sorted-bam]

outputs:
  oqc1:
    type: File
    outputSource: qc1/qc
  oqc2:
    type: File
    outputSource: qc2/qc
  oqc1P:
    type: File
    outputSource: qc1P/qc
  oqc2P:
    type: File
    outputSource: qc2P/qc
  sam:
    type: File
    outputSource: map/sam
  bam:
    type: File
    outputSource: sam2bam/bam
  osort:
    type: File
    outputSource: sort/sorted-bam
