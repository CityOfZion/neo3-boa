from typing import Any, Dict, Optional, Sized

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class IteratorConcatMethod(InteropMethod):
    def __init__(self, iterator: IteratorType, other_type: Optional[IteratorType] = None):
        syscall = 'System.Iterator.Concat'
        identifier = '-iterator_concat'

        iterator_type = IteratorType.build()
        if other_type is None:
            other_type = iterator_type
        args: Dict[str, Variable] = {'self': Variable(iterator),
                                     'other': Variable(other_type)}

        return_type = self._build_result(iterator, other_type)
        super().__init__(identifier, syscall, args, return_type=return_type)

    @property
    def identifier(self) -> str:
        return '{0}_{1}'.format(self.raw_identifier,
                                '_'.join([x.type.identifier for x in self.args.values()]))

    def _build_result(self, iterator: IteratorType, other_type: IteratorType) -> IType:
        if iterator == other_type:
            return iterator

        from boa3.model.type.type import Type
        key_type = Type.union.build([iterator.valid_key, other_type.valid_key])
        value_type = Type.union.build([iterator.value_type, other_type.value_type])

        new_collection = Type.dict.build([key_type, value_type])
        if new_collection.valid_key == iterator.valid_key and new_collection.value_type == iterator.value_type:
            return iterator

        elif new_collection.valid_key == other_type.valid_key and new_collection.value_type == other_type.value_type:
            return other_type

        return IteratorType.build(new_collection)

    def push_self_first(self) -> bool:
        return True

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, Sized) or len(value) != 2:
            return self

        iterator_type = IteratorType.build()
        self_type, other_type = value
        if not iterator_type.is_type_of(self_type) or not iterator_type.is_type_of(other_type):
            return self

        return IteratorConcatMethod(self_type, other_type)
