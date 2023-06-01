from typing import Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable


class StorageMapPutMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.builtin.interop.storage.storagemap.storagemaptype import _StorageMap
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.primitive.bytestringtype import ByteStringType

        identifier = 'put'
        byte_string_type = ByteStringType.build()

        args: Dict[str, Variable] = {'self': Variable(_StorageMap),
                                     'key': Variable(byte_string_type),
                                     'value': Variable(Type.union.build([byte_string_type,
                                                                         Type.int
                                                                         ]))}

        super().__init__(identifier, args, return_type=Type.none)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.model.operation.binaryop import BinaryOp

        # actual_key = self._prefix + key
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(1)
        code_generator.convert_get_item(index_inserted_internally=True)  # self._prefix

        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)

        # actual_context = self._context
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_literal(0)
        code_generator.convert_get_item(index_inserted_internally=True)  # self._context

        # return put(actual_key, actual_context)
        code_generator.convert_builtin_method_call(Interop.StoragePut, is_internal=True)
