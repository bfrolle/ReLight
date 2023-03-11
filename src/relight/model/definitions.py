from enum import Enum
from typing import Generator, List, NamedTuple, Tuple

XDIST: int = 250
XOFFSET: int = 34
YDIST: int = 80

CHANNEL: List[str] = ["red", "green", "blue", "alpha"]


class Point(NamedTuple):
    x: int = 0
    y: int = 0


class NodeType(Enum):
    COLOR_CORRECT = "ColorCorrect"
    DOT = "Dot"
    GRADE = "Grade"
    MERGE = "Merge"
    SHUFFLE = "Shuffle2"
    GROUP = "Group"

    @classmethod
    def value_generator(cls) -> Generator[str, None, None]:
        for element in cls:
            yield element.value

    @classmethod
    def value_tuple(cls) -> Tuple[str, ...]:
        return (value for value in cls.value_generator())
