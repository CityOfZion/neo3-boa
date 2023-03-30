from __future__ import annotations

import ast
from enum import Enum, auto
from typing import Optional, Union

from boa3.internal.model.operation.operation import IOperation
from boa3.internal.model.operation.operator import Operator


class Operation(Enum):
    Add = auto()
    Sub = auto()
    Mult = auto()
    Div = auto()
    FloorDiv = auto()
    Mod = auto()

    @property
    def is_symmetric(self) -> bool:
        return self._symmetric

    @classmethod
    def get_operation(cls, op: Union[ast.operator, IOperation]) -> Optional[Operation]:
        op = op.operator if isinstance(op, IOperation) else op
        if op is Operator.Plus or isinstance(op, (ast.Add, ast.UAdd)):
            return cls.Add
        elif op is Operator.Minus or isinstance(op, (ast.Sub, ast.USub)):
            return cls.Sub
        elif op is Operator.Mult or isinstance(op, ast.Mult):
            return cls.Mult
        elif op is Operator.Div or isinstance(op, ast.Div):
            return cls.Div
        elif op is Operator.IntDiv or isinstance(op, ast.FloorDiv):
            return cls.FloorDiv
        elif op is Operator.Mod or isinstance(op, ast.Mod):
            return cls.Mod
