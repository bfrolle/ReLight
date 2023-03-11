import re
from typing import Tuple

import nuke

from relight.model.category import Category
from relight.model.definitions import NodeType
from relight.utils import scan
from relight.utils.knobs import TabGroup

GRADE_KNOBS = ["blackpoint", "whitepoint", "black", "white", "multiply", "mix"]
COLLOR_COORECT_CAT = ["master", "shadows", "midtones", "highlights"]
COLLOR_CORRECT_KNOBS = ["saturation", "contrast", "gamma", "gain", "offset"]
COLLOR_CORRECT_RANGES = ["lookup", "mix"]

NUMBER_OF_KNOBS = (
    len(COLLOR_COORECT_CAT) * len(COLLOR_CORRECT_KNOBS)
    + len(GRADE_KNOBS)
    + len(COLLOR_CORRECT_RANGES)
)


def add(name: str, root: nuke.Node, category: Category) -> None:
    with TabGroup(name, root) as tab:
        tab.add_divider(name + ".upper_divider")

        for cc_ in COLLOR_COORECT_CAT:
            knob_prefix = f"{cc_}." if not cc_ == "master" else ""
            with TabGroup(cc_, root, prefix=name) as sub_tab:
                node = category.get_node(NodeType.COLOR_CORRECT, 0)
                for kn_ in COLLOR_CORRECT_KNOBS:
                    sub_tab.add_knob(node.knob(knob_prefix + kn_))

        with TabGroup("ranges", root, prefix=name) as sub_tab:
            node = category.get_node(NodeType.COLOR_CORRECT, 0)
            for kn_ in COLLOR_CORRECT_RANGES:
                sub_tab.add_knob(node.knob(kn_))

        with TabGroup("grade0", root, prefix=name) as sub_tab:
            node = category.get_node(NodeType.GRADE, 0)
            for kn_ in GRADE_KNOBS:
                sub_tab.add_knob(node.knob(kn_))

        with TabGroup("grade1", root, prefix=name) as sub_tab:
            node = category.get_node(NodeType.GRADE, 1)
            for kn_ in GRADE_KNOBS:
                sub_tab.add_knob(node.knob(kn_))

        tab.add_divider(name + ".lower_divider")


def remove(name: str, root: nuke.Node) -> None:
    in_category = False
    for knob in root.allKnobs():
        cat_match = re.search(f"^{name}$", knob.name())
        if cat_match and (not in_category):
            in_category = True
        elif cat_match and in_category:
            in_category = False
            root.removeKnob(knob)
            break
        if in_category:
            root.removeKnob(knob)


def reset(root: nuke.Node, with_prefix: Tuple[str, ...]) -> None:
    rm = list(with_prefix)
    rm.extend(GRADE_KNOBS)
    rm.extend(COLLOR_COORECT_CAT)
    rm.extend(COLLOR_CORRECT_KNOBS)
    rm.extend(COLLOR_CORRECT_RANGES)
    knobs = (kn for kn in root.allKnobs() if scan.filter_ps(kn.name(), rm))
    for kn_ in knobs:
        root.removeKnob(kn_)
