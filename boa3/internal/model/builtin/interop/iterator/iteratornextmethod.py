from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.internal.model.variable import Variable


class IteratorNextMethod(InteropMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        syscall = 'System.Iterator.Next'
        identifier = '-iterator_next'
        args: dict[str, Variable] = {'self': Variable(IteratorType.build())}
        super().__init__(identifier, syscall, args, return_type=Type.bool)
