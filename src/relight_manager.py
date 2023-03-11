from typing import List, Optional, Tuple, Union

import nuke

import relight_node
from relight.model import category_knobs
from relight.model.category import Category
from relight.model.definitions import XDIST, NodeType, Point
from relight.model.primitive import Primitive
from relight.utils import connect, names, place

CATDIST: int = XDIST


class Manager(Primitive):
    layer: Optional[Tuple[str, ...]] = None

    def __init__(self, position: Point = Point(x=0, y=0)) -> None:
        self.layer = relight_node.include_layer()
        self.nodes = None
        self.input, self.output = relight_node.interface()
        super().__init__("relight", position)
        if self.has_categories():
            categories = self.get_workspace_categories(self.input)
            self.elements = {}
            for cat in categories:
                self.add_element(cat, Category.scan(cat))

    @staticmethod
    def get_workspace_categories(
        input_node: nuke.Node, categories: Optional[List[str]] = None
    ) -> List[str]:
        if categories is None:
            categories = []
        dependent_nodes = input_node.dependent()
        origin_suffix = "_Dot_0"
        origins = (
            node for node in dependent_nodes if node.name().endswith(origin_suffix)
        )
        try:
            input_ = next(origins)
            category = names.remove_suffix(input_.name(), origin_suffix)
            categories.append(category)
            Manager.get_workspace_categories(input_, categories)
        except StopIteration:
            pass
        return categories

    def has_categories(self) -> bool:
        input_dependant = self.input.dependent()
        if not input_dependant:
            return False
        if input_dependant:
            if self.output.name() in (nd.name() for nd in input_dependant):
                return False
        return True

    def _check_category(self, name: str) -> Category:
        if not name in self.elements:
            raise AttributeError(f"Category '{name}' does not exist.")
        return self.elements[name]

    def successor(self, category: Category) -> Union[None, Category]:
        index = self.get_index(category.name)
        if index is None:
            return index
        if len(self) > index + 1:
            return self[index + 1]
        return None

    def predecessor(self, category: Category) -> Union[None, Category]:
        index = self.get_index(category.name)
        if index is None:
            return index
        if index > 0:
            return self[index - 1]
        return None

    def add_category(self, name: str) -> Category:
        if not name in self.layer:
            err_msg = f"Could not add category '{name}'. Select category from:"
            for layer in self.layer:
                err_msg += f"\n {layer}"
            raise AttributeError(err_msg)
        if name in self.elements:
            raise AttributeError(f"Category {name} already added.")
        new_category = self.add_element(name, Category(name))
        if self.has_categories():
            merge = new_category.add_node(NodeType.MERGE)
            merge["operation"].setValue("plus")
            predecessor = self.predecessor(new_category)
            new_category.connect_start(predecessor.origin)
            new_category.connect_end(self.output)
            new_category.position = Point(x=predecessor.x0 + CATDIST, y=predecessor.y0)
            connect.connect_nodes(predecessor.endnode, merge, 1)
        else:
            new_category.add_node(NodeType.DOT)
            new_category._set_node_positions()
            new_category.connect_start(self.input)
            new_category.connect_end(self.output)
            new_category.position = Point(x=self.x0, y=self.y0)
            place.place_node_above(self.input, new_category.origin)

        place.place_node_below(self.output, new_category.endnode)
        return new_category

    def remove_cateogry(self, name: str) -> None:
        category = self._check_category(name)
        successor = self.successor(category)
        predecessor = self.predecessor(category)

        if len(self) > 1:
            place.move_node_in_x(self.output, -CATDIST)

        def _move_all_successors(cat: Category) -> None:
            successor = self.successor(cat)
            if successor is not None:
                successor.move_nodes(xdist=-CATDIST)
                _move_all_successors(successor)

        _move_all_successors(category)
        category.remove()
        if predecessor is None:
            if successor is None:
                connect.connect_nodes(self.input, self.output)
                place.place_node_below(self.output, self.input)
            else:
                successor.remove_node(NodeType.MERGE, 0)
                successor.add_node(NodeType.DOT)
                successor._set_node_positions()
                successor.connect_start(self.input)
                successor.connect_end(self.output)
                place.place_node_below(self.output, self[-1].endnode)
        else:
            if successor is None:
                connect.connect_nodes(predecessor.endnode, self.output)
                place.place_node_below(self.output, predecessor.endnode)
            else:
                predecessor.connect_start(successor.origin)
                connect.connect_nodes(predecessor.endnode, successor.endnode, 1)
                place.place_node_below(self.output, self[-1].endnode)

    def add_category_knobs(self, name: str) -> None:
        category = self._check_category(name)
        root = nuke.thisNode()
        root.setTab(0)
        category_knobs.add(name=name, root=root, category=category)

    def remove_category_knobs(self, name: str) -> None:
        self._check_category(name)
        root = nuke.thisNode()
        category_knobs.remove(name, root)

    def _reset_categories(self):
        for category in self:
            category.remove()
        self.elements = {}

    def _reset_knobs(self):
        root = nuke.thisNode()
        category_knobs.reset(root, self.layer)

    def _reset_default(self):
        root = nuke.thisNode()
        self.input, self.output = relight_node.interface()
        relight_node.knobs(root)

    @staticmethod
    def _get_selected_category() -> str:
        root = nuke.thisNode()
        category_knob = root.knob("category")
        return category_knob.value()

    def add_button(self) -> None:
        nuke.Undo().begin()
        category = self._get_selected_category()
        self.add_category(category)
        self.add_category_knobs(category)
        nuke.Undo().end()

    def remove_button(self) -> None:
        nuke.Undo().begin()
        category = self._get_selected_category()
        self.remove_cateogry(category)
        self.remove_category_knobs(category)
        nuke.Undo().end()

    def reset_button(self) -> None:
        nuke.Undo().begin()
        self._reset_default()
        self._reset_knobs()
        self._reset_categories()
        nuke.Undo().end()
