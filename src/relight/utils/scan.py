from typing import Dict, List, Tuple, Union

import nuke


def filter_ps(
    name: str,
    prefix: Union[None, str, List[str]],
    suffix: Union[None, str, List[str]] = None,
) -> bool:
    if not name:
        return False

    if (prefix is None) and (suffix is None):
        return True

    include = False
    if prefix is not None:
        if isinstance(prefix, str):
            return name.startswith(prefix)
        else:
            for fname in prefix:
                if name.startswith(fname):
                    include = True
                    break

    if suffix is not None:
        if isinstance(suffix, str):
            return name.endswith(suffix)
        else:
            for fname in suffix:
                if name.endswith(fname):
                    include = True
                    break

    return include


def find_workspace_nodes(
    node_prefix: Union[None, str, List[str]] = None,
    node_suffix: Union[None, str, List[str]] = None,
) -> Dict[str, nuke.Node]:
    nodescan = (
        node
        for node in nuke.allNodes()
        if filter_ps(node.name(), node_prefix, node_suffix)
    )
    workspace_nodes = {}
    try:
        node = next(nodescan)
        workspace_nodes[node.name()] = node
    except StopIteration:
        return None

    for node in nodescan:
        workspace_nodes[node.name()] = node
    return workspace_nodes


def find_workspace_layer(
    layer_prefix: Union[None, str, List[str]] = None,
    layer_suffix: Union[None, str, List[str]] = None,
) -> Tuple[str, ...]:
    return tuple(
        layer for layer in nuke.layers() if filter_ps(layer, layer_prefix, layer_suffix)
    )
