class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  edam: "http://edamontology.org/"
baseCommand: fastqc
inputs:
  - id: fastq
    type: File
    format: edam:format_1930
    inputBinding:
      position: 2
    doc: FastQ file from next-generation sequencers
  - id: nthreads
    type: int?
    default: 2
    inputBinding:
      prefix: --threads
    doc: number of cpu cores to be used

outputs:
  - id: qc
    type: File
    outputBinding:
      glob: "*_fastqc.html"
label: fastqc
arguments:
  - position: 1
    prefix: -o
    valueFrom: .
hints:
  - class: DockerRequirement
    dockerPull: "quay.io/biocontainers/fastqc:0.11.7--pl5.22.0_2"
