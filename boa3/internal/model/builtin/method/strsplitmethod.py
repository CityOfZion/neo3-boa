import ast
from typing import Dict, List, Tuple

from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StrSplitMethod(StdLibMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'split'
        syscall = 'stringSplit'
        args: Dict[str, Variable] = {
            'self': Variable(Type.str),
            'sep': Variable(Type.str),
            'maxsplit': Variable(Type.int)
        }
        # whitespace is the default separator
        separator_default = ast.parse("' '").body[0].value
        # maxsplit the default value is -1
        maxsplit_default = ast.parse("-1").body[0].value.operand
        maxsplit_default.n = -1

        neo_internal_args = {
            'str': Variable(Type.str),
            'separator': Variable(Type.str),
            # TODO: include removeEmptyEntries
        }

        super().__init__(identifier, syscall, args, defaults=[separator_default, maxsplit_default],
                         return_type=Type.list.build_collection(Type.str),
                         internal_call_args=len(neo_internal_args))

    @property
    def generation_order(self) -> List[int]:
        # the original string must be the top value in the stack
        indexes = list(range(len(self.args)))
        str_index = list(self.args).index('self')

        if indexes[-1] != str_index:
            # context must be the last generated argument
            indexes.remove(str_index)
            indexes.append(str_index)
        return indexes

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.compiler.codegenerator import get_bytes_count
        from boa3.internal.model.type.type import Type

        jmp_place_holder = (Opcode.JMP, b'\x01')

        preserver_args_from_array = [   # copies split and maxsplit args on the stack
            OpcodeHelper.get_push_and_data(2),
            (Opcode.PICK, b''),
            (Opcode.SWAP, b''),
        ]

        neo_strsplit_method = super()._opcode

        verify_maxsplit = [     # verifies if there is a maxsplit
            (Opcode.OVER, b''),
            (Opcode.PUSHM1, b''),
            jmp_place_holder    # if maxsplit <= -1 skip concatenation and clean the stack
        ]

        while_verify = [        # verifies if len(array) <= maxsplit + 1, if it is jump out of while
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.INC, b''),
            jmp_place_holder    # go clean the stack
        ]

        concatenate_array = [
            (Opcode.DUP, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.POPITEM, b''),
            (Opcode.CAT, b''),
            (Opcode.OVER, b''),
            (Opcode.POPITEM, b''),
            (Opcode.SWAP, b''),
            (Opcode.CAT, b''),
            (Opcode.CONVERT, Type.str.stack_item),
            (Opcode.APPEND, b''),
            # go to while_verify
        ]

        num_jmp_code = -get_bytes_count(while_verify + concatenate_array)
        jmp_back_to_while = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code)
        concatenate_array.append(jmp_back_to_while)

        num_jmp_code = get_bytes_count(while_verify + concatenate_array)
        jmp_to_clean_from_verify_maxsplit = OpcodeHelper.get_jump_and_data(Opcode.JMPLE, num_jmp_code, True)
        verify_maxsplit[-1] = jmp_to_clean_from_verify_maxsplit

        num_jmp_code = get_bytes_count(concatenate_array)
        jmp_to_clean_from_while_verify = OpcodeHelper.get_jump_and_data(Opcode.JMPLE, num_jmp_code, True)
        while_verify[-1] = jmp_to_clean_from_while_verify

        clean_stack = [
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]

        return (
            preserver_args_from_array +
            neo_strsplit_method +
            verify_maxsplit +
            while_verify +
            concatenate_array +
            clean_stack
        )
