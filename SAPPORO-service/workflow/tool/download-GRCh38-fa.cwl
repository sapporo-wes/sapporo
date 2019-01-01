#!/usr/bin/env cwl-runner

class: CommandLineTool
id: download-GRCh38-fa
label: download-GRCh38-fa
cwlVersion: v1.0

$namespaces:
  edam: "http://edamontology.org/"

hints: []

baseCommand: [wget]

inputs: []

outputs:
  - id: ref
    type: File
    format: edam:format_1929
    outputBinding:
      glob: GRCh38_full_analysis_set_plus_decoy_hla.fa

arguments:
  - position: 1
    valueFrom: "http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa"
