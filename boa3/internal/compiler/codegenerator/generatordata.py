from __future__ import annotations

import ast
from typing import Optional

from boa3.internal.model.expression import IExpression
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType


class GeneratorData:

    def __init__(self, origin_node: Optional[ast.AST],
                 symbol_id: Optional[str] = None,
                 symbol: Optional[ISymbol] = None,
                 result_type: Optional[IType] = None,
                 index: Optional[int] = None,
                 origin_object_type: Optional[IType] = None,
                 already_generated: bool = False):

        if symbol_id is None and isinstance(symbol, IdentifiedSymbol):
            symbol_id = symbol.identifier
        if result_type is None and isinstance(symbol, IExpression):
            result_type = symbol.type

        self.node: Optional[ast.AST] = origin_node
        self.symbol: Optional[ISymbol] = symbol
        self.symbol_id: Optional[str] = symbol_id
        self.type: Optional[IType] = result_type
        self.index: Optional[int] = index
        self.origin_object_type: Optional[ISymbol] = origin_object_type
        self.already_generated: bool = already_generated

    def copy(self, new_origin: Optional[ast.AST] = None) -> GeneratorData:
        return GeneratorData(new_origin if isinstance(new_origin, ast.AST) else self.node,
                             self.symbol_id,
                             self.symbol,
                             self.type,
                             self.index,
                             self.already_generated)
