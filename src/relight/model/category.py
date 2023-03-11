import nuke

from relight.model.definitions import CHANNEL, NodeType
from relight.model.node_string import NodeString


class Category(NodeString):
    def __init__(self, name: str, x0: int = 0, y0: int = 0) -> None:
        super().__init__(name, x0, y0)

    def build(self) -> None:
        category_nodes = (
            NodeType.DOT,
            NodeType.SHUFFLE,
            NodeType.COLOR_CORRECT,
            NodeType.GRADE,
            NodeType.GRADE,
        )
        nodes = (nd for nd in category_nodes)
        self.add_origin(next(nodes))
        for nd in nodes:
            self.add_node(nd)
        self._set_properties()

    def _set_properties(self) -> None:
        if not self.name in nuke.layers():
            nuke.Layer(self.name, CHANNEL)

        shuffle = self.get_node(NodeType.SHUFFLE, 0)
        shuffle["in1"].setValue(self.name)

    @classmethod
    def scan(cls, name: str):
        category = cls.__new__(cls)
        setattr(category, "name", name)
        origin = category.get_node(NodeType.DOT, 0)
        return cls.from_workpace(name, origin)
