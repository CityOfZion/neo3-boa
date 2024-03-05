from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.variable import Variable


class StorageMapGetMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.builtin.interop.storage.storagemap.storagemaptype import _StorageMap
        from boa3.internal.model.type.type import Type

        identifier = 'get'
        args: dict[str, Variable] = {'self': Variable(_StorageMap),
                                     'key': Variable(Type.bytes)}

        super().__init__(identifier, args, return_type=Type.bytes)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def self_type(self):
        """
        :rtype: boa3.internal.model.builtin.interop.storage.storagemap.storagemaptype.StorageMapType
        """
        return self.args['self'].type

    @property
    def _body(self) -> str | None:
        return None

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.model.operation.binaryop import BinaryOp

        # actual_key = self._prefix + key
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_load_class_variable(self.self_type, '_prefix', is_internal=True)  # self._prefix

        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)

        # actual_context = self._context
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_load_class_variable(self.self_type, '_context', is_internal=True)  # self._context

        # return get(actual_key, actual_context)
        code_generator.convert_builtin_method_call(Interop.StorageGet, is_internal=True)
