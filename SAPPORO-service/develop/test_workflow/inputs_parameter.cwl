#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow

inputs:
  input_boolean:
    type: boolean
  input_boolean_default:
    type: boolean?
    default: true
  input_int:
    type: int
  input_int_default:
    type: int?
    default: 1
  input_long:
    type: long
  input_long_default:
    type: long?
    default: 1000000000000
  input_float:
    type: float
  input_float_default:
    type: float?
    default: 10.0
  input_double:
    type: double
  input_double_default:
    type: double?
    default: 10000000000000000000000000000000000000000000000000
  input_string:
    type: string
  input_string_default:
    type: string?
    default: default_string
  input_File:
    type: File
  input_File_default:
    type: File?
    default: ./test.txt
  input_Directory:
    type: Directory
  input_Directory_default:
    type: Directory?
    default: ./test_dir

steps: []
outputs: []
