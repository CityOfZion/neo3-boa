from typing import Dict

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.model.variable import Variable


class GetIteratorValue(InteropMethod):
    def __init__(self, iterator: IteratorType):
        syscall = 'System.Enumerator.Value'
        identifier = '-get_iterator_value'
        args: Dict[str, Variable] = {'self': Variable(iterator)}
        super().__init__(identifier, syscall, args, return_type=iterator.item_type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)


class IteratorValueProperty(IBuiltinProperty):
    def __init__(self, iterator: IteratorType):
        identifier = 'iterator_value'
        getter = GetIteratorValue(iterator)
        super().__init__(identifier, getter)
