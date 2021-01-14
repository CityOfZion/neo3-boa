from typing import Any, Dict, Optional, Sized

from boa3.model.builtin.interop.enumerator.enumeratortype import EnumeratorType
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class EnumeratorConcatMethod(InteropMethod):
    def __init__(self, enumerator: EnumeratorType, other_type: Optional[EnumeratorType] = None):
        syscall = 'System.Enumerator.Concat'
        identifier = '-enumerator_concat'

        if other_type is None:
            other_type = EnumeratorType.build()
        args: Dict[str, Variable] = {'self': Variable(enumerator),
                                     'other': Variable(other_type)}

        return_type = self._build_result(enumerator, other_type)
        super().__init__(identifier, syscall, args, return_type=return_type)

    @property
    def identifier(self) -> str:
        return '{0}_{1}'.format(self.raw_identifier,
                                '_'.join([x.type.identifier for x in self.args.values()]))

    def _build_result(self, enumerator: EnumeratorType, other_type: EnumeratorType) -> IType:
        if enumerator == other_type:
            return enumerator

        from boa3.model.type.type import Type
        value_type = Type.union.build([enumerator.value_type, other_type.value_type])

        new_sequence = Type.list.build([value_type])
        if new_sequence.value_type == enumerator.value_type:
            return enumerator

        elif new_sequence.value_type == other_type.value_type:
            return other_type

        return EnumeratorType.build(new_sequence)

    def push_self_first(self) -> bool:
        return True

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, Sized) or len(value) != 2:
            return self

        enumerator_type = EnumeratorType.build()
        self_type, other_type = value
        if not enumerator_type.is_type_of(self_type) or not enumerator_type.is_type_of(other_type):
            return self

        return EnumeratorConcatMethod(self_type, other_type)
