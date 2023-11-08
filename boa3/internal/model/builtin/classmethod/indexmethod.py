import ast
from typing import Any, Dict, List, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable


class IndexMethod(IBuiltinMethod):

    def __init__(self, args: Dict[str, Variable] = None, defaults: List[ast.AST] = None):
        from boa3.internal.model.type.type import Type
        identifier = 'index'
        super().__init__(identifier, args, defaults=defaults, return_type=Type.int)

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type

        if self._arg_self.type is Type.sequence:  # IndexSequenceMethod default value for self
            return self._identifier

        if self._arg_self.type is Type.str:
            return '-{0}_{1}'.format(self._identifier, Type.str.identifier)

        if Type.sequence.is_type_of(self._arg_self.type):
            return '-{0}_{1}'.format(self._identifier, Type.sequence.identifier)

        return self._identifier

    @property
    def is_supported(self) -> bool:
        # TODO: change when index() with only one argument is implemented for range #2kq1y13
        from boa3.internal.model.type.type import Type
        if Type.range.is_type_of(self._arg_self.type):
            return False
        return True

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def _arg_value(self) -> Variable:
        return self.args['value']

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, list):
            value = [value]

        from boa3.internal.model.type.collection.sequence.mutable.listtype import ListType
        from boa3.internal.model.type.collection.sequence.tupletype import TupleType
        from boa3.internal.model.type.collection.sequence.rangetype import RangeType
        if len(value) > 1 and isinstance(value[0], (ListType, TupleType, RangeType)):
            from boa3.internal.model.builtin.classmethod.indexsequencemethod import IndexSequenceMethod
            return IndexSequenceMethod(value[0], value[1])

        from boa3.internal.model.type.type import Type
        if len(value) > 0 and (Type.str.is_type_of(value[0]) or Type.bytes.is_type_of(value[0])):
            from boa3.internal.model.builtin.classmethod.indexbytesstringmethod import IndexBytesStringMethod
            return IndexBytesStringMethod(value[0])

        return super().build(value)
