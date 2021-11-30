from typing import List, Optional, Tuple

from boa3.model.builtin.classmethod.copymethod import CopyMethod
from boa3.model.type.itype import IType
from boa3.neo.vm.opcode.Opcode import Opcode


class CopyDictMethod(CopyMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.model.type.type import Type
        super().__init__(arg_value if Type.dict.is_type_of(arg_value) else Type.dict)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.compiler.codegenerator import get_bytes_count

        jmp_place_holder = (Opcode.JMP, b'\x01')

        create_auxiliary_vars = [       # initializes auxiliary variables
            (Opcode.NEWMAP, b''),       # dict_copy = {}
            (Opcode.OVER, b''),
            (Opcode.KEYS, b''),         # list_keys = list(dict_target)
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),
            (Opcode.DEC, b''),          # index = len(list_keys) - 1
        ]

        verify_while_condition = [      # if index < 0: go clean stack
            (Opcode.DUP, b''),
            (Opcode.PUSH0, b''),
            jmp_place_holder            # jump to clean_stack
        ]

        while_loop = [                  # while index >= 0: add key value pair into new dict
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PICKITEM, b''),     # key = list_keys[index]
            (Opcode.PUSH5, b''),
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b''),     # value = dict_target[key]
            (Opcode.SETITEM, b''),      # dict_copy[key] = value
            (Opcode.DEC, b''),          # index--
            # jump back to verify_while_condition
        ]

        jmp_back_to_verify = Opcode.get_jump_and_data(Opcode.JMP, -get_bytes_count(while_loop + verify_while_condition))
        while_loop.append(jmp_back_to_verify)

        jmp_while_loop = Opcode.get_jump_and_data(Opcode.JMPLT, get_bytes_count(while_loop))
        verify_while_condition[-1] = jmp_while_loop

        clean_stack = [                 # remove all values from stack except the dict_copy
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            (Opcode.NIP, b'')
        ]

        return (
            create_auxiliary_vars +
            verify_while_condition +
            while_loop +
            clean_stack
        )
