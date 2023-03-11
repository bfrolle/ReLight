from typing import Any, Generator, Union

from relight.model.definitions import Point


class Primitive:
    def __init__(self, name: str, position: Point) -> None:
        self.name = name
        self.elements = {}
        self._position = position

    def __len__(self) -> int:
        return len(self.elements)

    def __iter__(self) -> Generator[Any, None, None]:
        for node in self.elements.values():
            yield node

    def __getitem__(self, indx: int) -> Any:
        return tuple(self.elements.values())[indx]

    def add_element(self, name: str, element: Any) -> Any:
        if name in self.elements:
            raise TypeError(f"Could not add element '{name}'.")
        self.elements[name] = element
        return element

    def remove_element(self, name: str):
        if not name in self.elements:
            raise TypeError(f"Could not remove element '{name}'.")
        self.elements.pop(name)

    def get_index(self, element_name: str) -> Union[None, int]:
        if element_name in self.elements:
            return list(self.elements.keys()).index(element_name)
        return None

    @property
    def x0(self) -> int:
        return self._position.x

    @property
    def y0(self) -> int:
        return self._position.y

    @property
    def prefix(self) -> str:
        return f"{self.name}_"
