from typing import Tuple

import nuke

from relight.utils import connect, place, scan
from relight.utils.knobs import divider_knob, python_script_knob

NAME = "piRelight"
INCLUDE_LAYER = ["light", "Light", "LIGHT"]


def new_name() -> str:
    node_prefix = NAME
    nodes_of_type = scan.find_workspace_nodes(node_prefix)
    if nodes_of_type:
        node_names_of_type = sorted(list(nodes_of_type.keys()))
        last_name_of_type = node_names_of_type[-1]
        last_node_number = last_name_of_type.split("_")[-1]
        node_number = int(last_node_number) + 1
    else:
        node_number = 0
    return f"{node_prefix}_{node_number}"


def interface() -> Tuple[nuke.Node, nuke.Node]:
    input_name = "AOV"
    input_scan = scan.find_workspace_nodes(node_prefix=input_name)
    input_node = input_scan.get(input_name, None) if input_scan else None
    if input_node is None:
        nuke.nodes.Input(name=input_name)
        input_node = nuke.toNode(input_name)

    output_name = "Beauty"
    output_scan = scan.find_workspace_nodes(node_prefix=output_name)
    output_node = output_scan.get(output_name, None) if output_scan else None
    if output_node is None:
        nuke.nodes.Output(name=output_name)
        output_node = nuke.toNode(output_name)

    place.place_node_below(output_node, input_node)

    return input_node, output_node


def include_layer() -> Tuple[str, ...]:
    return scan.find_workspace_layer(
        layer_prefix=INCLUDE_LAYER, layer_suffix=INCLUDE_LAYER
    )


def knobs(root: nuke.Node) -> None:
    knobs_ = root.knobs()
    # Relight Tab
    tab_kn_name = "tab_relight"
    if not tab_kn_name in knobs_:
        root.addKnob(nuke.Tab_Knob(tab_kn_name, "Relight"))

    # Dropdown for category selection
    layer = include_layer()
    category_kn_name = "category"
    if not category_kn_name in knobs_:
        root.addKnob(
            nuke.CascadingEnumeration_Knob(category_kn_name, "select category:", layer)
        )
    else:
        knobs_.get(category_kn_name).setValues(list(layer))

    # Python category control buttons
    for button in ["add", "remove"]:
        kn = python_script_knob(
            label=button,
            script=(
                "from relight_manager import Manager\n"
                f"man = Manager()\nman.{button}_button()"
            ),
            tool_tip=f"{button.capitalize()} selected category",
        )
        if not kn.name() in knobs_:
            root.addKnob(kn)

    # Python reset button
    kn = python_script_knob(
        label="reset",
        script=(
            "from relight_manager import Manager\n"
            "man = Manager()\nman.reset_button()"
        ),
        tool_tip=(
            "Reset all categories.\n"
            "Note that all categories and settings will be removed."
        ),
    )
    if not kn.name() in knobs_:
        root.addKnob(kn)

    # Divider knob
    kn = divider_knob("relight_divider")
    if not kn.name() in knobs_:
        root.addKnob(kn)


def create() -> nuke.Node:
    node_name = new_name()
    root = nuke.nodes.Group(name=node_name)
    with root:
        input_node, output_node = interface()
        connect.connect_nodes(input_node, output_node)
    knobs(root)
    return root
