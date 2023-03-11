from abc import ABC, abstractmethod
from typing import Dict, List, NamedTuple, Optional, Tuple

import nuke

from relight.model.definitions import NodeType, Point
from relight.model.primitive import Primitive
from relight.utils import connect, names, place


class Node(NamedTuple):
    type: NodeType
    number: int
    prefix: str = ""

    @property
    def name(self) -> str:
        return names.node_name(self.type, self.number, self.prefix)


class NodeString(ABC, Primitive):
    def __init__(self, name: str, x0: int, y0: int) -> None:
        super().__init__(name, Point(x0, y0))

        self._nodes = None
        self._node_names = None

        self.build()
        self._set_node_positions()

    @abstractmethod
    def build(self) -> None:
        pass

    @classmethod
    def from_workpace(cls, name: str, origin: nuke.Node):
        nodestring = cls.__new__(cls)
        setattr(nodestring, "name", name)
        setattr(nodestring, "elements", {})
        setattr(nodestring, "_position", None)
        setattr(nodestring, "_nodes", None)
        setattr(nodestring, "_node_names", None)
        workspaceNodes = nodestring.get_workspaceNodes(origin)
        for nd in workspaceNodes:
            nodestring.add_element(nd.name, nodestring.get_node(nd.type, nd.number))
        nodestring.origin = origin
        return nodestring

    @property
    def origin(self) -> nuke.Node:
        return self[0]

    @origin.setter
    def origin(self, node: nuke.Node) -> None:
        if node.name() in self.elements:
            self.elements.pop(node.name())
        nodes = {node.name(): node}
        nodes.update(self.elements)
        setattr(self, "elements", nodes)
        self._reset_properties()
        self.position = Point(x=node.xpos(), y=node.ypos())
        self._reconnect()

    @property
    def endnode(self) -> nuke.Node:
        return self[-1]

    @property
    def position(self) -> Point:
        return self._position

    @position.setter
    def position(self, value: Point) -> None:
        self._position = value
        self._set_node_positions()

    @property
    def nodes(self) -> Tuple[nuke.Node, ...]:
        if self._nodes is None:
            self._nodes = tuple(node for node in iter(self))
        return self._nodes

    @property
    def node_names(self) -> Tuple[str, ...]:
        if self._node_names is None:
            self._node_names = tuple(name for name in self.elements)
        return self._node_names

    def _reset_properties(self):
        self._nodes = None
        self._node_names = None

    def _reconnect(self) -> None:
        nodes = iter(self)
        last_node = next(nodes)
        for node in nodes:
            connect.connect_nodes(last_node, node)
            last_node = node

    def _set_node_positions(self) -> None:
        place.move_node_to(self.origin, self.x0, self.y0)
        nodes = iter(self)
        last_node = next(nodes)
        for node in nodes:
            place.place_node_below(node, last_node)
            last_node = node

    def move_nodes(
        self, xdist: Optional[int] = None, ydist: Optional[int] = None
    ) -> None:
        x0 = self.x0
        y0 = self.y0
        if xdist is not None:
            x0 += xdist
        if ydist is not None:
            y0 += ydist
        self.position = Point(x0, y0)

    def get_nodes_of_type(self, type: NodeType) -> Dict[str, nuke.Node]:
        search_name = names.node_type_name(type, self.prefix)
        nodes_of_type = {
            name: node for name, node in self.elements.items() if search_name in name
        }
        sorted_node_names = sorted(list(nodes_of_type.keys()))
        return {name: nodes_of_type[name] for name in sorted_node_names}

    def get_node(self, type: NodeType, number: int) -> nuke.Node:
        name = names.node_name(type, number, self.prefix)
        return nuke.toNode(name)

    def add_origin(self, type: NodeType) -> nuke.Node:
        if self.elements:
            raise TypeError(
                f"Node string '{self.name}' already has an origin: {self.origin.name()}"
            )
        name = names.new_node_name(type, self.prefix)
        self.add_element(name, getattr(nuke.nodes, type.value)(name=name))
        return self.elements[name]

    def add_node(
        self,
        type: NodeType,
        input: int = 0,
    ) -> nuke.Node:
        name = names.new_node_name(type, self.prefix)
        new_node = getattr(nuke.nodes, type.value)(name=name)
        connect.connect_nodes(self[-1], new_node, input)
        self.add_element(name, new_node)
        self._reset_properties()

        return new_node

    def remove_node(self, type: NodeType, number: int = 0) -> None:
        node = self.get_node(type, number)
        self.elements.pop(node.name())
        nuke.delete(node)
        self._reset_properties()

    def remove(self):
        for node in self.elements.values():
            nuke.delete(node)
        self.elements = {}
        self._reset_properties()

    def connect_start(self, node: nuke.Node, input: int = 0) -> None:
        connect.connect_nodes(node, self.origin, input)

    def connect_end(self, node: nuke.Node, input: int = 0) -> None:
        connect.connect_nodes(self.endnode, node, input)

    def get_workspaceNodes(
        self, input: nuke.Node, nodes: Optional[List[Node]] = None
    ) -> List[Node]:
        if nodes is None:
            origin_type, origin_number = names.get_node_type_and_number(
                input, self.prefix
            )
            nodes = [Node(origin_type, origin_number, self.prefix)]
        dependent_nodes = input.dependent()
        origins = (
            node for node in dependent_nodes if node.name().startswith(self.prefix)
        )
        try:
            input_ = next(origins)
            node_type, node_number = names.get_node_type_and_number(input_, self.prefix)
            nodes.append(Node(node_type, node_number, self.prefix))
            self.get_workspaceNodes(input_, nodes)
        except StopIteration:
            pass
        return nodes
