import nuke


def connect_nodes(
    src_node: nuke.Node, dest_node: nuke.Node, dest_input: int = 0
) -> None:
    dest_node.setInput(dest_input, src_node)
