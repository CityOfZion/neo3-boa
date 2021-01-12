from typing import Dict

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.model.variable import Variable


class GetIteratorKey(InteropMethod):
    def __init__(self, iterator: IteratorType):
        syscall = 'System.Iterator.Key'
        identifier = '-get_iterator_key'
        args: Dict[str, Variable] = {'self': Variable(iterator)}
        super().__init__(identifier, syscall, args, return_type=iterator.valid_key)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)


class IteratorKeyProperty(IBuiltinProperty):
    def __init__(self, iterator: IteratorType):
        identifier = 'iterator_key'
        getter = GetIteratorKey(iterator)
        super().__init__(identifier, getter)
