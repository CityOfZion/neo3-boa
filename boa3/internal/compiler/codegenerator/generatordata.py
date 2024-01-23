from __future__ import annotations

import ast

from boa3.internal.model.expression import IExpression
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType


class GeneratorData:

    def __init__(self, origin_node: ast.AST | None,
                 symbol_id: str | None = None,
                 symbol: ISymbol | None = None,
                 result_type: IType | None = None,
                 index: int | None = None,
                 origin_object_type: IType | None = None,
                 already_generated: bool = False):

        if symbol_id is None and isinstance(symbol, IdentifiedSymbol):
            symbol_id = symbol.identifier
        if result_type is None and isinstance(symbol, IExpression):
            result_type = symbol.type

        self.node: ast.AST | None = origin_node
        self.symbol: ISymbol | None = symbol
        self.symbol_id: str | None = symbol_id
        self.type: IType | None = result_type
        self.index: int | None = index
        self.origin_object_type: ISymbol | None = origin_object_type
        self.already_generated: bool = already_generated

    def copy(self, new_origin: ast.AST | None = None) -> GeneratorData:
        return GeneratorData(new_origin if isinstance(new_origin, ast.AST) else self.node,
                             self.symbol_id,
                             self.symbol,
                             self.type,
                             self.index,
                             self.already_generated)
