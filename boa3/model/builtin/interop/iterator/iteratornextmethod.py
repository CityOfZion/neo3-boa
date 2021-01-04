from typing import Dict, List, Tuple

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class IteratorNextMethod(InteropMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        syscall = 'System.Enumerator.Next'
        identifier = '-iterator_next'
        args: Dict[str, Variable] = {'self': Variable(IteratorType.build())}
        super().__init__(identifier, syscall, args, return_type=Type.bool)
