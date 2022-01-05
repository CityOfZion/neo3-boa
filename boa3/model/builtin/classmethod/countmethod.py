import ast
from typing import Any, Dict, List, Optional

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable


class CountMethod(IBuiltinMethod):

    def __init__(self, args: Dict[str, Variable] = None, defaults: List[ast.AST] = None):
        from boa3.model.type.type import Type
        identifier = 'count'
        super().__init__(identifier, args, defaults=defaults, return_type=Type.int)

    @property
    def identifier(self) -> str:
        from boa3.model.type.type import Type

        if self._arg_self.type is Type.sequence:  # CountSequenceMethod default value for self
            return self._identifier

        if self._arg_self.type is Type.str:
            return '-{0}_{1}'.format(self._identifier, Type.str.identifier)

        if Type.sequence.is_type_of(self._arg_self.type):
            return '-{0}_{1}'.format(self._identifier, Type.sequence.identifier)

        return self._identifier

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

        from boa3.model.type.collection.sequence.mutable.listtype import ListType
        from boa3.model.type.collection.sequence.tupletype import TupleType
        from boa3.model.type.collection.sequence.rangetype import RangeType
        if len(value) > 1 and isinstance(value[0], (ListType, TupleType, RangeType)):
            from boa3.model.builtin.classmethod.countsequencemethod import CountSequenceMethod
            return CountSequenceMethod(value[0], value[1])

        from boa3.model.type.type import Type
        if len(value) > 0 and Type.str.is_type_of(value[0]):
            from boa3.model.builtin.builtin import Builtin
            return Builtin.CountStr

        return super().build(value)
