# coding: utf-8
import yaml
from collections import OrderedDict

yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, lambda loader, node: OrderedDict(loader.construct_pairs(node)))


def parse_cwl_input_params(cwl_file):
    """
    inputs: cwl_file -> str
    outputs: input_params -> list
        {
            label: str
            type: str (boolean, int, float, string)
                - int, long, double -> int
                - string, File, Directoru -> string
            default: str, boolean, int, float, None
            doc: str or None
        }
    """
    d_cwl_file = yaml.load(cwl_file)
    assert "inputs" in d_cwl_file, "CWL file does not have inputs field."
    input_params = []
    for label, d_values in d_cwl_file["inputs"].items():
        assert "type" in d_values, "The content of CWL file is incorrect"
        input_param = dict()
        input_param["label"] = label
        if d_values["type"].strip("?") in ["int", "long", "double"]:
            input_param["type"] = "int"
        elif d_values["type"].strip("?") in ["string", "File", "Directory"]:
            input_param["type"] = "string"
        else:
            input_param["type"] = d_values["type"].strip("?")
        if "default" in d_values:
            input_param["default"] = d_values["default"]
        else:
            input_param["default"] = None
        if "doc" in d_values:
            input_param["doc"] = d_values["doc"]
        else:
            if "label" in d_values:
                input_param["doc"] = d_values["label"]
            else:
                input_param["doc"] = None
        input_params.append(input_param)

    return input_params
