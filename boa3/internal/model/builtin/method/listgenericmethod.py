import ast
from typing import Dict, List, Tuple

from boa3.internal.model.builtin.method.listmethod import ListMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ListGenericMethod(ListMethod):

    def __init__(self, value: IType = None):
        from boa3.internal.model.type.type import Type

        if value is None:
            value = Type.any

        args: Dict[str, Variable] = {
            'value': Variable(value),
        }

        value_default = ast.parse("{0}".format(Type.sequence.default_value)
                                  ).body[0].value

        return_value = Type.any if value is Type.any else []

        if return_value is not Type.any:
            for type_ in value.union_types:
                if type_ is Type.str:
                    return_value.append(Type.str)
                elif type_ is Type.bytes:
                    return_value.append(Type.int)
                elif Type.sequence.is_type_of(type_):
                    return_value.append(type_.value_type)
                elif Type.mapping.is_type_of(type_):
                    return_value.append(type_.key_type)

            if Type.str in value.union_types and Type.bytes in value.union_types:
                return_value.remove(Type.str)

        return_type = Type.list.build_collection(return_value)

        super().__init__(args, return_type, [value_default])

    @property
    def prepare_for_packing(self) -> List[Tuple[Opcode, bytes]]:

        if self._prepare_for_packing is None:
            from boa3.internal.compiler.codegenerator import get_bytes_count
            from boa3.internal.neo.vm.type.StackItem import StackItemType
            from boa3.internal.model.type.annotation.uniontype import UnionType
            from boa3.internal.model.type.type import Type
            from boa3.internal.neo.vm.type.Integer import Integer
            from boa3.internal.neo.vm.type.String import String

            jmp_place_holder = (Opcode.JMP, b'\x01')
            error_message = String('Invalid value given, it should be an iterable').to_bytes()

            verify_is_bytes_string = [
                (Opcode.DUP, b''),
                (Opcode.ISTYPE, StackItemType.ByteString),
                jmp_place_holder
            ]

            from boa3.internal.model.builtin.method import ListBytesStringMethod
            if isinstance(self._arg_value, UnionType) and \
                    Type.str in self._arg_value.union_types and Type.bytes not in self._arg_value.union_types:
                pre_packing_bytes_string = ListBytesStringMethod(Type.str).prepare_for_packing
            else:
                pre_packing_bytes_string = ListBytesStringMethod().prepare_for_packing

            verify_is_sequence = [
                (Opcode.DUP, b''),
                (Opcode.ISTYPE, StackItemType.Array),
                jmp_place_holder
            ]

            from boa3.internal.model.builtin.method import ListSequenceMethod
            pre_packing_sequence = ListSequenceMethod().prepare_for_packing

            verify_is_mapping = [
                (Opcode.DUP, b''),
                (Opcode.ISTYPE, StackItemType.Map),
                jmp_place_holder
            ]

            from boa3.internal.model.builtin.method import ListMappingMethod
            pre_packing_mapping = ListMappingMethod().prepare_for_packing

            invalid_value = [
                (Opcode.PUSHDATA1, Integer(len(error_message)).to_byte_array(signed=True) + error_message),
                (Opcode.THROW, b'')
            ]

            num_jmp_code = get_bytes_count(invalid_value)
            jmp_to_end_from_mapping = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code, True)
            pre_packing_mapping.append(jmp_to_end_from_mapping)

            num_jmp_code = get_bytes_count(pre_packing_mapping)
            jmp_prepare_mapping = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, num_jmp_code, True)
            verify_is_mapping.append(jmp_prepare_mapping)

            num_jmp_code = get_bytes_count(invalid_value + pre_packing_mapping + verify_is_mapping)
            jmp_to_end_from_sequence = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code, True)
            pre_packing_sequence.append(jmp_to_end_from_sequence)

            num_jmp_code = get_bytes_count(pre_packing_sequence)
            jmp_prepare_sequence = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, num_jmp_code, True)
            verify_is_sequence.append(jmp_prepare_sequence)

            num_jmp_code = get_bytes_count(invalid_value + pre_packing_mapping + verify_is_mapping +
                                           pre_packing_sequence + verify_is_sequence)
            jmp_to_end_from_bytes_string = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code, True)
            pre_packing_bytes_string.append(jmp_to_end_from_bytes_string)

            num_jmp_code = get_bytes_count(pre_packing_bytes_string)
            jmp_prepare_bytes_string = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, num_jmp_code, True)
            verify_is_bytes_string.append(jmp_prepare_bytes_string)

            self._prepare_for_packing = (
                verify_is_bytes_string +
                pre_packing_bytes_string +
                verify_is_sequence +
                pre_packing_sequence +
                verify_is_mapping +
                pre_packing_mapping +
                invalid_value
            )

        return super().prepare_for_packing
