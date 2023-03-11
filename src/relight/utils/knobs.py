import traceback
from typing import Optional

import nuke


def python_script_knob(
    label: str, script: str, tool_tip: str = ""
) -> nuke.PyScript_Knob:
    kn = nuke.PyScript_Knob(f"py_button_{label.lower()}", label, script)
    if tool_tip:
        kn.setTooltip(tool_tip)
    return kn


def divider_knob(name: str) -> nuke.Text_Knob:
    divider_str = "- " * 20
    return nuke.Text_Knob(name, "", divider_str)


class TabGroup:
    def __init__(
        self, name: str, node: Optional[nuke.Node] = None, prefix: str = ""
    ) -> None:
        self.node = nuke.thisNode() if node is None else node
        self.name = f"{prefix}.{name}" if prefix else name
        self.label = f"{name}:"
        self.knob = nuke.Tab_Knob(self.name, self.label, nuke.TABBEGINGROUP)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()
        if exc_type:
            print(f"An exception occured in the TabGroup context: {exc_type}")
            traceback.print_tb(exc_tb)
            raise exc_value

    def open(self):
        self.node.addKnob(self.knob)

    def add_knob(self, knob: nuke.Knob) -> None:
        self.node.addKnob(knob)

    def add_divider(self, name: str):
        self.node.addKnob(divider_knob(name))

    def close(self):
        self.node.addKnob(nuke.Tab_Knob(self.name, self.label, nuke.TABENDGROUP))
