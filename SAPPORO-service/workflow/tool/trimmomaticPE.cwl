#!/usr/bin/env cwl-runner

class: CommandLineTool
id: trimmomatic-0.38
label: trimmomatic-0.38
cwlVersion: v1.0

$namespaces:
  edam: "http://edamontology.org/"

hints:
  - class: DockerRequirement
    dockerPull: "quay.io/biocontainers/trimmomatic:0.38--1"

baseCommand: [java, -jar]

inputs:
  - id: nthreads
    type: int?
    default: 2
    inputBinding:
      prefix: -threads
      position: 3
    doc: number of cpu cores to be used
  - id: fq1
    type: File
    format: edam:format_1930
    inputBinding:
      position: 4
    doc: FastQ file from next-generation sequencers
  - id: fq2
    type: File
    format: edam:format_1930
    inputBinding:
      position: 5
    doc: FastQ file from next-generation sequencers

outputs:
  - id: trimFq1P
    type: File
    format: edam:format_1930
    outputBinding:
      glob: $(inputs.fq1.basename).trim.1P.fastq
  - id: trimFq1U
    type: File
    format: edam:format_1930
    outputBinding:
      glob: $(inputs.fq1.basename).trim.1U.fastq
  - id: trimFq2P
    type: File
    format: edam:format_1930
    outputBinding:
      glob: $(inputs.fq2.basename).trim.2P.fastq
  - id: trimFq2U
    type: File
    format: edam:format_1930
    outputBinding:
      glob: $(inputs.fq2.basename).trim.2U.fastq

arguments:
  - position: 1
    valueFrom: /usr/local/share/trimmomatic/trimmomatic.jar
  - position: 2
    valueFrom: PE
  - position: 6
    valueFrom: $(inputs.fq1.basename).trim.1P.fastq
  - position: 7
    valueFrom: $(inputs.fq1.basename).trim.1U.fastq
  - position: 8
    valueFrom: $(inputs.fq2.basename).trim.2P.fastq
  - position: 9
    valueFrom: $(inputs.fq2.basename).trim.2U.fastq
  - position: 10
    valueFrom: "ILLUMINACLIP:/usr/local/share/trimmomatic/adapters/TruSeq2-PE.fa:2:40:15"
