import ast
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable


class CountMethod(IBuiltinMethod):

    def __init__(self, args: dict[str, Variable] = None, defaults: list[ast.AST] = None):
        from boa3.internal.model.type.type import Type
        identifier = 'count'
        super().__init__(identifier, args, defaults=defaults, return_type=Type.int)

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type

        if self._arg_self.type is Type.str:     # CountStrMethod
            return '-{0}_{1}'.format(self._identifier, Type.str.identifier)

        if Type.sequence.is_type_of(self._arg_self.type):

            from boa3.internal.model.type.annotation.uniontype import UnionType
            from boa3.internal.model.type.primitive.bytestype import BytesType
            from boa3.internal.model.type.primitive.inttype import IntType
            from boa3.internal.model.type.primitive.strtype import StrType

            if isinstance(self._arg_self.type.value_type, (BytesType, IntType, StrType)) or\
                    ((isinstance(self._arg_self.type.value_type, UnionType) and
                      all(isinstance(type_, (BytesType, IntType, StrType)) for type_ in self._arg_self.type.value_type.union_types))):    # CountSequencePrimitiveValueMethod
                return '-{0}_{1}'.format(self._identifier, 'primitive')

            elif Type.mutableSequence.is_type_of(self._arg_self.type.value_type):    # CountSequenceGenericValueMethod
                return self._identifier

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
    def _body(self) -> str | None:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, list):
            value = [value]

        from boa3.internal.model.type.collection.sequence.mutable.listtype import ListType
        from boa3.internal.model.type.collection.sequence.tupletype import TupleType
        from boa3.internal.model.type.collection.sequence.rangetype import RangeType
        if len(value) > 1 and isinstance(value[0], (ListType, TupleType, RangeType)):

            from boa3.internal.model.type.primitive.bytestype import BytesType
            from boa3.internal.model.type.primitive.inttype import IntType
            from boa3.internal.model.type.primitive.strtype import StrType
            from boa3.internal.model.type.annotation.uniontype import UnionType

            if isinstance(value[0].value_type, (BytesType, IntType, StrType)) or\
                    ((isinstance(value[0].value_type, UnionType) and
                      all(isinstance(type_, (BytesType, IntType, StrType)) for type_ in value[0].value_type.union_types))):

                from boa3.internal.model.builtin.classmethod.countsequenceprimitivemethod import CountSequencePrimitiveMethod
                return CountSequencePrimitiveMethod(value[0], value[1])

            from boa3.internal.model.builtin.classmethod.countsequencegenericmethod import CountSequenceGenericMethod
            return CountSequenceGenericMethod(value[0], value[1])

        from boa3.internal.model.type.type import Type
        if len(value) > 0 and Type.str.is_type_of(value[0]):
            from boa3.internal.model.builtin.builtin import Builtin
            return Builtin.CountStr

        return super().build(value)
