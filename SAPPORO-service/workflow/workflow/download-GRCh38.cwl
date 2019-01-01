#!/usr/bin/env cwl-runner

class: Workflow
id: download-GRCh38
label: download-GRCh38
cwlVersion: v1.0

$namespaces:
  edam: "http://edamontology.org/"

inputs: []

steps:
  download-fa:
    label: download-fa
    doc: Download reference FastA file
    run: ../tool/download-GRCh38-fa.cwl
    in: []
    out: [ref]

  download-alt:
    label: download-alt
    doc: Download reference ALT file
    run: ../tool/download-GRCh38-alt.cwl
    in: []
    out: [alt]

  bwa-index:
    label: bwa-index
    doc: Create INDEX for bwa
    run: ../tool/bwa-index.cwl
    in:
      fa: download-fa/ref
    out: [amb, ann, bwt, pac, sa]

outputs:
  ref:
    type: File
    outputSource: download-fa/ref
  alt:
    type: File
    outputSource: download-alt/alt
  amb:
    type: File
    outputSource: bwa-index/amb
  ann:
    type: File
    outputSource: bwa-index/ann
  bwt:
    type: File
    outputSource: bwa-index/bwt
  pac:
    type: File
    outputSource: bwa-index/pac
  sa:
    type: File
    outputSource: bwa-index/sa
