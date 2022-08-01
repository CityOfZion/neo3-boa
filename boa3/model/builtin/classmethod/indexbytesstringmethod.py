import ast
from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.classmethod.indexmethod import IndexMethod
from boa3.model.expression import IExpression
from boa3.model.type.primitive.bytestype import BytesType
from boa3.model.type.primitive.strtype import StrType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String


class IndexBytesStringMethod(IndexMethod):

    def __init__(self, self_type: Optional[StrType] = None):
        from boa3.model.type.type import Type
        if not isinstance(self_type, (StrType, BytesType)):
            self_type = Type.str

        args: Dict[str, Variable] = {
            'self': Variable(self_type),
            'x': Variable(self_type),
            'start': Variable(Type.int),
            'end': Variable(Type.int),
        }

        start_default = ast.parse("{0}".format(0)
                                  ).body[0].value
        end_default = ast.parse("-1").body[0].value.operand
        end_default.n = -1

        super().__init__(args, defaults=[start_default, end_default])

    def validate_parameters(self, *params: IExpression) -> bool:
        if 2 <= len(params) <= 4:
            return False
        if not all(isinstance(param, IExpression) for param in params):
            return False

        from boa3.model.type.itype import IType
        self_type: IType = params[0].type

        if not isinstance(self_type, (StrType, BytesType)):
            return False

        if not self_type.is_type_of(params[1]):
            return False

        return True

    @property
    def error_message(self) -> str:
        return 'substring not found' if isinstance(self._arg_self.type, StrType) else 'subsequence of bytes not found'

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.compiler.codegenerator import get_bytes_count
        from boa3.neo.vm.type.StackItem import StackItemType

        jmp_place_holder = (Opcode.JMP, b'\x01')
        message = String(self.error_message).to_bytes()

        # receives: end, start, substr, str
        verify_negative_index = [           # verifies if index in a negative value
            (Opcode.DUP, b''),
            (Opcode.PUSHM1, b''),
            jmp_place_holder                # if index >= 0, jump to verify_big_end or verify_big_start
        ]

        fix_negative_end = [                # gets the correspondent positive value of end
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
            (Opcode.ADD, b''),
            (Opcode.INC, b''),              # end = end + len(str) + 1
            (Opcode.DUP, b''),
            (Opcode.PUSHM1, b''),
            jmp_place_holder                # if end is not negative anymore, start verifying start
        ]

        fix_still_negative_index = [        # if index is still negative, consider it 0 then
            (Opcode.DROP, b''),
            (Opcode.PUSH0, b''),            # end = 0
        ]

        jmp_fix_negative_index = Opcode.get_jump_and_data(Opcode.JMPGT, get_bytes_count(fix_negative_end +
                                                                                        fix_still_negative_index), True)
        verify_negative_index[-1] = jmp_fix_negative_index

        verify_big_end = [                  # verify if end is bigger then len(str)
            (Opcode.DUP, b''),
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
            jmp_place_holder                # if end <= len(str), start verifying start
        ]

        fix_big_end = [                     # consider end as len(str)
            (Opcode.DROP, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),             # end = len(str)
        ]

        jmp_other_verifies = Opcode.get_jump_and_data(Opcode.JMPGT, get_bytes_count(fix_still_negative_index +
                                                                                    verify_big_end +
                                                                                    fix_big_end), True)
        fix_negative_end[-1] = jmp_other_verifies

        jmp_fix_big_index = Opcode.get_jump_and_data(Opcode.JMPLE, get_bytes_count(fix_big_end), True)
        verify_big_end[-1] = jmp_fix_big_index

        verify_and_fix_end = [              # collection of Opcodes regarding verifying and fixing end index
            (Opcode.REVERSE4, b''),
        ]
        verify_and_fix_end.extend(verify_negative_index)
        verify_and_fix_end.extend(fix_negative_end)
        verify_and_fix_end.extend(fix_still_negative_index)
        verify_and_fix_end.extend(verify_big_end)
        verify_and_fix_end.extend(fix_big_end)

        verify_and_fix_start = [            # collection of Opcodes regarding verifying and fixing start index
            (Opcode.SWAP, b'')
        ]
        verify_and_fix_start.extend(verify_negative_index)
        verify_and_fix_start.extend(fix_negative_end)
        verify_and_fix_start.extend(fix_still_negative_index)
        verify_and_fix_start.extend(verify_big_end)
        verify_and_fix_start.extend(fix_big_end)

        change_stack_order = [              # change order of items on the stack
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),             # size = len(substr)
            (Opcode.ROT, b''),
            (Opcode.ROT, b''),
        ]

        verify_while = [                    # verify already compared all that was need
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            (Opcode.SUB, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            jmp_place_holder                # if end - index >= size, jump to not_inside_sequence
        ]

        compare_item = [                    # compare str[index:index+size] with substr
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, StackItemType.ByteString),
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.NUMEQUAL, b''),
            jmp_place_holder                # if str[index:index+size] == substr, return index
        ]

        not_found = [                       # increments index and goes back to verify again
            (Opcode.INC, b''),              # index++
            # jump to verify_while
        ]

        jmp_back_to_verify = Opcode.get_jump_and_data(Opcode.JMP, -get_bytes_count(verify_while +
                                                                                   compare_item +
                                                                                   not_found), True)
        not_found.append(jmp_back_to_verify)

        jmp_to_error = Opcode.get_jump_and_data(Opcode.JMPLT, get_bytes_count(compare_item +
                                                                              not_found), True)
        verify_while[-1] = jmp_to_error

        not_inside_sequence = [             # send error message saying that substring not found
            (Opcode.PUSHDATA1, Integer(len(message)).to_byte_array(signed=True, min_length=1) + message),
            (Opcode.THROW, b''),
        ]

        jmp_to_return_index = Opcode.get_jump_and_data(Opcode.JMPIF, get_bytes_count(not_found +
                                                                                     not_inside_sequence), True)
        compare_item[-1] = jmp_to_return_index

        return_index = [                    # removes all values in the stack but the index
            (Opcode.NIP, b''),
            (Opcode.NIP, b''),
            (Opcode.NIP, b''),
            (Opcode.NIP, b''),
        ]

        return (
            verify_and_fix_end +
            verify_and_fix_start +
            change_stack_order +
            verify_while +
            compare_item +
            not_found +
            not_inside_sequence +
            return_index
        )
