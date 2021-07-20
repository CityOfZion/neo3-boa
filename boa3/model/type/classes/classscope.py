import enum


class ClassScope(enum.Enum):
    STATIC = enum.auto()
    CLASS = enum.auto()
    INSTANCE = enum.auto()
