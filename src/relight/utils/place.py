import nuke

from relight.model.definitions import XDIST, YDIST


def move_node_in_x(node: nuke.Node, xdist: int) -> None:
    x0 = node.xpos()
    node.setXpos(x0 + xdist)


def move_node_in_y(node: nuke.Node, ydist: int) -> None:
    y0 = node.ypos()
    node.setYpos(y0 + ydist)


def move_node_to(node: nuke.Node, x: int, y: int) -> None:
    node.setXpos(x)
    node.setYpos(y)


def place_node_below(node: nuke.Node, origin: nuke.Node, ydist: int = YDIST) -> None:
    x0 = origin.xpos()
    y0 = origin.ypos()
    node.setXpos(x0)
    node.setYpos(y0 + ydist)


def place_node_above(node: nuke.Node, origin: nuke.Node, ydist: int = YDIST) -> None:
    x0 = origin.xpos()
    y0 = origin.ypos()
    node.setXpos(x0)
    node.setYpos(y0 - ydist)


def place_node_to_right(node: nuke.Node, origin: nuke.Node, xdist: int = XDIST) -> None:
    x0 = origin.xpos()
    y0 = origin.ypos()
    node.setXpos(x0 + xdist)
    node.setYpos(y0)


def place_node_to_left(node: nuke.Node, origin: nuke.Node, xdist: int = XDIST) -> None:
    x0 = origin.xpos()
    y0 = origin.ypos()
    node.setXpos(x0 - xdist)
    node.setYpos(y0)
