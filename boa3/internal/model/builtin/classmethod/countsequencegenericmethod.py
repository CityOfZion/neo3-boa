from typing import List, Optional, Tuple

from boa3.internal.model.builtin.classmethod.countsequencemethod import CountSequenceMethod
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class CountSequenceGenericMethod(CountSequenceMethod):

    def __init__(self, sequence_type: Optional[SequenceType] = None, arg_value: Optional[IType] = None):
        super().__init__(sequence_type, arg_value)

    def generic_verification(self, inc_statement_bytes=None,
                             get_equals_statement_bytes=None) -> List[Tuple[Opcode, bytes]]:

        if self._generic_verification_opcodes is None:
            jmp_place_holder = (Opcode.JMP, b'\x01')

            from boa3.internal.compiler.codegenerator import get_bytes_count
            from boa3.internal.model.type.type import Type

            sequence_verify_value_is_sequence = [  # verifies if value is a Sequence
                (Opcode.PUSH3, b''),
                (Opcode.PICK, b''),
                (Opcode.ISTYPE, Type.sequence.stack_item),
                jmp_place_holder,  # JMP to sequence_get_element if not
            ]

            sequence_verify_item_is_sequence = [  # verifies if the sequence[index] is a Sequence
                (Opcode.PUSH2, b''),
                (Opcode.PICK, b''),
                (Opcode.OVER, b''),
                (Opcode.PICKITEM, b''),
                (Opcode.ISTYPE, Type.sequence.stack_item),
                jmp_place_holder,  # jmp to list_tuple_count_index_dec if not
            ]

            sequence_verify_item_value_is_same_size = [  # verify if value and sequence[index] are the same size
                (Opcode.PUSH3, b''),
                (Opcode.PICK, b''),
                (Opcode.PUSH3, b''),
                (Opcode.PICK, b''),
                (Opcode.PUSH2, b''),
                (Opcode.PICK, b''),
                (Opcode.PICKITEM, b''),
                (Opcode.OVER, b''),
                (Opcode.SIZE, b''),
                (Opcode.OVER, b''),
                (Opcode.SIZE, b''),
                jmp_place_holder  # jmp to sequence_compare_sequences_initialize if true
            ]

            sequence_remove_aux_and_verify_next = [  # remove auxiliary values on stack and verify next item
                (Opcode.DROP, b''),
                (Opcode.DROP, b''),
                jmp_place_holder  # jumps to list_tuple_count_index_dec
            ]

            sequence_compare_sequences_initialize = [
                # starts another index for both sequences (value and sequence[índex])
                (Opcode.DUP, b''),
                (Opcode.SIZE, b''),
            ]

            sequence_compare_sequences_start = [  # compare both sequences
                (Opcode.DEC, b''),
                (Opcode.OVER, b''),
                (Opcode.OVER, b''),
                (Opcode.PICKITEM, b''),
                (Opcode.PUSH3, b''),
                (Opcode.PICK, b''),
                (Opcode.PUSH2, b''),
                (Opcode.PICK, b''),
                (Opcode.PICKITEM, b''),
                jmp_place_holder  # jumps to #sequence_compare_sequences_end_is_not_equal if they have different items
            ]

            sequence_compare_sequences_verify_end = [  # verify if all items were compared already
                (Opcode.DUP, b''),
                (Opcode.PUSH0, b''),
                # jumps to back to the verification if not
            ]

            sequence_compare_sequences_end_is_equal = [  # if they have the same values, then increment count
                (Opcode.DROP, b''),  # remove auxiliary values on stack
                (Opcode.DROP, b''),
                (Opcode.DROP, b''),
                jmp_place_holder  # jumps to sequence_count_inc
            ]

            sequence_compare_sequences_end_is_not_equal = [
                # if they do not have the same values go check the next item
                (Opcode.DROP, b''),
                (Opcode.DROP, b''),
                (Opcode.DROP, b''),
                jmp_place_holder  # jumps to list_tuple_count_index_dec
            ]

            num_jmp_code = inc_statement_bytes + get_equals_statement_bytes
            sequence_compare_sequences_end_is_not_equal[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code, True)

            num_jmp_code = get_bytes_count(sequence_compare_sequences_end_is_not_equal) + get_equals_statement_bytes
            sequence_compare_sequences_end_is_equal[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code, True)

            num_jmp_code = -get_bytes_count(sequence_compare_sequences_verify_end + sequence_compare_sequences_start)
            sequence_compare_sequences_verify_end.append(OpcodeHelper.get_jump_and_data(Opcode.JMPGT, num_jmp_code))

            num_jmp_code = get_bytes_count(sequence_compare_sequences_verify_end +
                                           sequence_compare_sequences_end_is_equal)
            sequence_compare_sequences_start[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPNE, num_jmp_code, True)

            num_jmp_code = get_bytes_count(
                sequence_compare_sequences_initialize + sequence_compare_sequences_start +
                sequence_compare_sequences_verify_end + sequence_compare_sequences_end_is_equal +
                sequence_compare_sequences_end_is_not_equal) + get_equals_statement_bytes + inc_statement_bytes
            sequence_remove_aux_and_verify_next[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code, True)

            num_jmp_code = get_bytes_count(sequence_remove_aux_and_verify_next)
            sequence_verify_item_value_is_same_size[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPEQ, num_jmp_code, True)

            num_jmp_code = get_bytes_count(
                sequence_verify_item_value_is_same_size + sequence_remove_aux_and_verify_next +
                sequence_compare_sequences_initialize + sequence_compare_sequences_start +
                sequence_compare_sequences_verify_end + sequence_compare_sequences_end_is_equal +
                sequence_compare_sequences_end_is_not_equal) + get_equals_statement_bytes + inc_statement_bytes
            sequence_verify_item_is_sequence[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, num_jmp_code, True)

            num_jmp_code = get_bytes_count(sequence_verify_item_is_sequence + sequence_verify_item_value_is_same_size +
                                           sequence_remove_aux_and_verify_next + sequence_compare_sequences_initialize +
                                           sequence_compare_sequences_start + sequence_compare_sequences_verify_end +
                                           sequence_compare_sequences_end_is_equal +
                                           sequence_compare_sequences_end_is_not_equal)
            sequence_verify_value_is_sequence[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, num_jmp_code, True)

            self._generic_verification_opcodes = (
                sequence_verify_value_is_sequence +
                sequence_verify_item_is_sequence +
                sequence_verify_item_value_is_same_size +
                sequence_remove_aux_and_verify_next +
                sequence_compare_sequences_initialize +
                sequence_compare_sequences_start +
                sequence_compare_sequences_verify_end +
                sequence_compare_sequences_end_is_equal +
                sequence_compare_sequences_end_is_not_equal
            )

        return super().generic_verification()
