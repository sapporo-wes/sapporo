#!/usr/bin/env cwl-runner

class: CommandLineTool
id: picard-mark-duplicates-2.18.20--0
label: picard-mark-duplicates-2.18.20--0
cwlVersion: v1.0

$namespaces:
  edam: "http://edamontology.org/"

hints:
  - class: DockerRequirement
    dockerPull: "quay.io/biocontainers/picard:2.18.20--0"

requirements:
  - class: ShellCommandRequirement

baseCommand: [java, -jar, /usr/local/share/picard-2.18.20-0/picard.jar, SortSam]

inputs:
  - id: bam
    type: File
    format: edam:format_2572
    inputBinding:
      prefix: "I="
      position: 1
    doc: BAM alignment file

outputs:
  - id: sorted-bam
    type: File
    format: edam:format_2572
    outputBinding:
      glob: output.sort.bam

arguments:
  - position: 2
    valueFrom: "O=output.sort.bam"
  - position: 3
    valueFrom: "SORT_ORDER=coordinate"
