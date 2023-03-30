from typing import Dict, List, Tuple

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class GetIteratorValue(InteropMethod):
    def __init__(self, iterator: IteratorType):
        syscall = 'System.Iterator.Value'
        identifier = '-get_iterator_value'
        args: Dict[str, Variable] = {'self': Variable(iterator)}

        result_type = iterator.item_type
        from boa3.internal.model.type.collection.mapping.mappingtype import MappingType
        if isinstance(iterator._origin_collection, MappingType):
            from boa3.internal.model.type.type import Type
            result_type = Type.tuple.build((iterator.key_type, iterator.item_type))
        super().__init__(identifier, syscall, args, return_type=result_type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def self_arg(self) -> Variable:
        return self.args['self']

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.neo.vm.type.StackItem import StackItemType
        from boa3.internal.neo.vm.type.Integer import Integer
        return super()._opcode + [
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, StackItemType.Struct),
            (Opcode.JMPIFNOT, Integer(3).to_byte_array()),
            (Opcode.CONVERT, StackItemType.Array),
        ]


class IteratorValueProperty(IBuiltinProperty):
    def __init__(self, iterator: IteratorType):
        identifier = 'iterator_value'
        getter = GetIteratorValue(iterator)
        super().__init__(identifier, getter)
