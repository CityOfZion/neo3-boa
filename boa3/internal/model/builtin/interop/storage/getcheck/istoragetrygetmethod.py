import abc

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.storage.neostorageinterop import NeoStorageInterop, StorageContextGet
from boa3.internal.model.operation.unaryop import UnaryOp
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class IStorageTryGetMethod(InteropMethod, abc.ABC):

    def __init__(self, identifier: str, value_type: IType, storage_interop: NeoStorageInterop = None):
        if storage_interop is None:
            self._storage_interop = StorageContextGet()
        else:
            self._storage_interop = storage_interop

        syscall = self._storage_interop.syscall_name()

        args, defaults = self._storage_interop.args_default()

        return_type = Type.tuple.build((value_type, Type.bool))
        super().__init__(identifier, syscall, args, defaults=defaults, return_type=return_type)

    @abc.abstractmethod
    def generate_default_value_opcodes(self, code_generator):
        pass

    @abc.abstractmethod
    def generate_deserialize_value_opcodes(self, code_generator):
        pass

    def generate_internal_opcodes(self, code_generator):
        super().generate_internal_opcodes(code_generator)

        # exists = result is not None
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(None)
        code_generator.convert_operation(UnaryOp.Not, is_internal=True)

        # if exists:
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_item(2)
        if_is_null = code_generator.convert_begin_if()

        #   result = deserialize(result)
        self.generate_deserialize_value_opcodes(code_generator)

        # else
        else_is_not_null = code_generator.convert_begin_else(if_is_null, is_internal=True)
        #   result = default_value
        code_generator.remove_stack_top_item()
        self.generate_default_value_opcodes(code_generator)

        if else_is_not_null < code_generator.last_code_start_address:
            if_is_null = else_is_not_null
        code_generator.convert_end_if(if_is_null, is_internal=True)

        code_generator.convert_new_array(2, self.return_type)

    @property
    def identifier(self) -> str:
        return self._storage_interop.new_identifier(self._identifier, str(self.key_arg.type))

    @property
    def generation_order(self) -> list[int]:
        """
        Gets the indexes order that need to be used during code generation.
        If the order for generation is the same as inputted in code, returns reversed(range(0,len_args))

        :return: Index order for code generation
        """
        indexes = super().generation_order

        return self._storage_interop.change_generation_order(indexes, self.args)

    @property
    def key_arg(self) -> Variable:
        return self.args['key']
