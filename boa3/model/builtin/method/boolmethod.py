from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class BoolMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'bool'

        args: Dict[str, Variable] = {
            'value': Variable(Type.any),
        }
        super().__init__(identifier, args, return_type=Type.bool)

    @property
    def _value(self) -> Variable:
        return self.args['value']

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.StackItem import StackItemType
        from boa3.compiler.codegenerator import get_bytes_count
        jmp_place_holder = (Opcode.JMP, b'\x01')

        verify_is_none = [  # verify if value is None
            (Opcode.DUP, b''),
            (Opcode.ISNULL, b''),
            jmp_place_holder
        ]

        value_is_none = [   # if value is None, then return False
            (Opcode.DROP, b''),
            (Opcode.PUSH0, b''),
            jmp_place_holder
        ]

        verify_is_array = [     # if value is an array, check the length of it
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, StackItemType.Array),
            jmp_place_holder
        ]

        verify_is_map = [       # if value is a map, check the length of it
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, StackItemType.Map),
            jmp_place_holder
        ]

        verify_is_int = [       # if value is an int, check if it is non zero
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, StackItemType.Integer),
            jmp_place_holder
        ]

        verify_is_bytestring = [    # if value is a bytestring, check if it is non zero
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, StackItemType.ByteString),
            jmp_place_holder
        ]

        put_true = [    # if value it's not a type from above, return True
            (Opcode.DROP, b''),
            (Opcode.PUSH1, b''),
            jmp_place_holder
        ]

        collection_non_zero = [     # get length of collection
            (Opcode.SIZE, b''),
        ]

        non_zero = [        # verify if it's non zero
            (Opcode.NZ, b''),
        ]

        # region jump logic

        jump_instructions = collection_non_zero + non_zero
        put_true[-1] = Opcode.get_jump_and_data(Opcode.JMP, get_bytes_count(jump_instructions), True)

        jump_instructions = collection_non_zero + put_true
        verify_is_bytestring[-1] = Opcode.get_jump_and_data(Opcode.JMPIF, get_bytes_count(jump_instructions), True)

        jump_instructions = collection_non_zero + put_true + verify_is_bytestring
        verify_is_int[-1] = Opcode.get_jump_and_data(Opcode.JMPIF, get_bytes_count(jump_instructions), True)

        jump_instructions = put_true + verify_is_int + verify_is_bytestring
        verify_is_map[-1] = Opcode.get_jump_and_data(Opcode.JMPIF, get_bytes_count(jump_instructions), True)

        jump_instructions = verify_is_map + verify_is_int + verify_is_bytestring + put_true
        verify_is_array[-1] = Opcode.get_jump_and_data(Opcode.JMPIF, get_bytes_count(jump_instructions), True)

        jump_instructions = (
            verify_is_array +
            verify_is_map +
            verify_is_int +
            verify_is_bytestring +
            put_true +
            collection_non_zero +
            non_zero
        )
        value_is_none[-1] = Opcode.get_jump_and_data(Opcode.JMP, get_bytes_count(jump_instructions), True)

        jump_instructions = value_is_none
        verify_is_none[-1] = Opcode.get_jump_and_data(Opcode.JMPIFNOT, get_bytes_count(jump_instructions), True)

        # endregion

        bool_method = (
            verify_is_none +
            value_is_none +
            verify_is_array +
            verify_is_map +
            verify_is_int +
            verify_is_bytestring +
            put_true +
            collection_non_zero +
            non_zero
        )

        return bool_method

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
