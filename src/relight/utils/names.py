import copy
from typing import Tuple

import nuke

from relight.model.definitions import NodeType
from relight.utils.scan import find_workspace_nodes


def remove_suffix(input_string: str, suffix: str) -> str:
    if suffix and input_string.endswith(suffix):
        return input_string[: -len(suffix)]
    return copy.copy(input_string)


def remove_prefix(input_string: str, prefix: str) -> str:
    if prefix and input_string.startswith(prefix):
        return input_string[len(prefix) :]
    return copy.copy(input_string)


def node_type_name(type: NodeType, prefix: str = "") -> str:
    node_name_ = type.value
    if prefix:
        return f"{prefix}{node_name_}"
    return node_name_


def node_name(type: NodeType, number: int, prefix: str = "") -> str:
    return f"{node_type_name(type, prefix)}_{number}"


def new_node_name(type: NodeType, prefix: str = "") -> str:
    node_prefix = node_type_name(type, prefix)
    nodes_of_type = find_workspace_nodes(node_prefix)
    if nodes_of_type:
        node_names_of_type = sorted(list(nodes_of_type.keys()))
        last_name_of_type = node_names_of_type[-1]
        last_node_number = last_name_of_type.split("_")[-1]
        node_number = int(last_node_number) + 1
    else:
        node_number = 0
    return node_name(type, node_number, prefix)


def get_node_type_and_number(node: nuke.Node, prefix: str = "") -> Tuple[NodeType, int]:
    node_name_ = remove_prefix(node.name(), prefix)
    name_parts = node_name_.split("_")
    node_type = name_parts[0]
    node_number = name_parts[-1]
    return NodeType(node_type), int(node_number)
