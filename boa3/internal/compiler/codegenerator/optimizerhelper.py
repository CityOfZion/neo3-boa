__all__ = [
    'OptimizationLevel',
    'is_storing_static_variable'
]

import enum

from boa3.internal.model.variable import Variable


class OptimizationLevel(enum.IntEnum):
    NONE = enum.auto()
    DEBUG = enum.auto()
    HIGH = enum.auto()

    DEFAULT = HIGH


def is_storing_static_variable(level: OptimizationLevel, var: Variable) -> bool:
    if not hasattr(var, '_set_as_global'):
        var._set_as_global = not var.is_reassigned and var.has_literal_value

    if level <= OptimizationLevel.DEBUG:
        return True

    # doesn't store variables that we know the value on higher optimization levels
    return var.is_reassigned or not var.has_literal_value
