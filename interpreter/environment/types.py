from enum import auto, Enum


class Types(Enum):
    NUMBER = 0
    FLOAT = 1
    STRING = 2
    BOOLEAN = 3
    CHAR = 4
    NULL = 5

    ARRAY = auto()
    INTERFACE = auto()
