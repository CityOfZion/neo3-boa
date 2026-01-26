import abc

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.storage.neostorageinterop import NeoStorageInterop, StorageContextPut
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class IStoragePutMethod(InteropMethod, abc.ABC):

    def __init__(self, identifier: str, value_type: IType, storage_interop: NeoStorageInterop = None):
        if storage_interop is None:
            self._storage_interop = StorageContextPut()
        else:
            self._storage_interop = storage_interop

        syscall = self._storage_interop.syscall_name()

        args, defaults = self._storage_interop.args_default(value_type)

        super().__init__(identifier, syscall, args, defaults=defaults, return_type=Type.none)

    @abc.abstractmethod
    def generate_serialize_value_opcodes(self, code_generator):
        pass

    def generate_internal_opcodes(self, code_generator):
        start_address = code_generator.bytecode_size
        if self.identifier.endswith(self._storage_interop.CONTEXT_SUFFIX):
            code_generator.swap_reverse_stack_items(3)
        elif self.identifier.endswith(self._storage_interop.LOCAL_SUFFIX):
            code_generator.swap_reverse_stack_items(2)
        self.generate_serialize_value_opcodes(code_generator)
        end_address = code_generator.last_code_start_address

        if end_address > start_address:
            if self.identifier.endswith(self._storage_interop.CONTEXT_SUFFIX):
                code_generator.swap_reverse_stack_items(3)
            elif self.identifier.endswith(self._storage_interop.LOCAL_SUFFIX):
                code_generator.swap_reverse_stack_items(2)
        else:
            code_generator._remove_inserted_opcodes_since(start_address)

        super().generate_internal_opcodes(code_generator)

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

    @property
    def value_arg(self) -> Variable:
        return self.args['value']
