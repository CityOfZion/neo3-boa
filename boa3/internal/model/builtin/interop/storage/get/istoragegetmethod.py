import abc

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.storage.neostorageinterop import NeoStorageInterop, StorageContextGet
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class IStorageGetMethod(InteropMethod, abc.ABC):

    def __init__(self, identifier: str, value_type: IType, storage_interop: NeoStorageInterop = None):
        if storage_interop is None:
            self._storage_interop = StorageContextGet()
        else:
            self._storage_interop = storage_interop

        syscall = self._storage_interop.syscall_name()

        args, defaults = self._storage_interop.args_default()

        super().__init__(identifier, syscall, args, defaults=defaults, return_type=value_type)

    @abc.abstractmethod
    def generate_default_value_opcodes(self, code_generator):
        pass

    @abc.abstractmethod
    def generate_deserialize_value_opcodes(self, code_generator):
        pass

    def generate_internal_opcodes(self, code_generator):
        super().generate_internal_opcodes(code_generator)
        # if result is None:
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(None)
        if_is_null = code_generator.convert_begin_if()

        #   result = default_value
        code_generator.remove_stack_top_item()
        self.generate_default_value_opcodes(code_generator)

        else_is_null = code_generator.convert_begin_else(if_is_null, is_internal=True)
        self.generate_deserialize_value_opcodes(code_generator)

        if else_is_null < code_generator.last_code_start_address:
            if_is_null = else_is_null
        code_generator.convert_end_if(if_is_null, is_internal=True)

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
