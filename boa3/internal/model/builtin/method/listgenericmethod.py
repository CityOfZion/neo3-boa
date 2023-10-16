import ast
from typing import Dict

from boa3.internal.model.builtin.method.listmethod import ListMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


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

    def generate_pack_opcodes(self, code_generator):
        from boa3.internal.model.builtin.method import ListBytesStringMethod
        from boa3.internal.model.type.annotation.uniontype import UnionType
        from boa3.internal.model.type.type import Type
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        error_message = 'Invalid value given, it should be an iterable'

        # if instance(value, str)
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(StackItemType.ByteString)
        is_byte_string = code_generator.convert_begin_if()

        #   byte string implementation
        (ListBytesStringMethod(Type.str)
         if (isinstance(self._arg_value.type, UnionType) and
             Type.str in self._arg_value.type.union_types and
             Type.bytes not in self._arg_value.type.union_types)
         else ListBytesStringMethod()
         ).generate_pack_opcodes(code_generator)

        is_byte_string = code_generator.convert_begin_else(is_byte_string, is_internal=True)
        # elif isinstance(value, list):
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(StackItemType.Array)
        is_list = code_generator.convert_begin_if()

        #   list implementation
        from boa3.internal.model.builtin.method import ListSequenceMethod
        ListSequenceMethod().generate_pack_opcodes(code_generator)

        is_list = code_generator.convert_begin_else(is_list, is_internal=True)
        # elif isinstance(value, map):
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(StackItemType.Map)
        is_map = code_generator.convert_begin_if()

        #   map implementation
        from boa3.internal.model.builtin.method import ListMappingMethod
        ListMappingMethod().generate_pack_opcodes(code_generator)

        is_map = code_generator.convert_begin_else(is_map, is_internal=True)
        # else:
        code_generator.convert_literal(error_message)
        # raise error
        code_generator.convert_raise_exception()

        code_generator.convert_end_if(is_map, is_internal=True)
        code_generator.convert_end_if(is_list, is_internal=True)
        code_generator.convert_end_if(is_byte_string, is_internal=True)
