import abc

from boa3.internal import constants
from boa3.internal.model.type.classes import classtype
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.StackItem import StackItemType


class PythonClass(classtype.ClassType, abc.ABC):

    def __init__(self, identifier: str,
                 instance_variables: dict = None,
                 instance_methods: dict = None,
                 properties: dict = None,
                 class_variables: dict = None,
                 class_methods: dict = None,
                 static_methods: dict = None):

        self._instance_methods = instance_methods if isinstance(instance_methods, dict) else None
        self._instance_variables = instance_variables if isinstance(instance_variables, dict) else None
        self._properties = properties if isinstance(properties, dict) else None
        self._class_variables = class_variables if isinstance(class_variables, dict) else None
        self._class_methods = class_methods if isinstance(class_methods, dict) else None
        self._static_methods = static_methods if isinstance(static_methods, dict) else None

        is_init_defined = isinstance(instance_methods, dict) and constants.INIT_METHOD_ID in instance_methods
        self._is_init_set = is_init_defined
        self._constructor = (instance_methods[constants.INIT_METHOD_ID]
                             if is_init_defined
                             else None)

        super().__init__(identifier)

    def _init_class_symbols(self):
        """
        Overwrite this method to set variables and methods from this type.
        Always call super()._init_class_symbols in the beginning
        Used to avoid circular imports between the init classes
        """
        # TODO: May be removed when class inheritance is implemented #2kq1ght
        if not isinstance(self._instance_methods, dict):
            self._instance_methods = {}
        if not isinstance(self._instance_variables, dict):
            self._instance_variables = {}
        if not isinstance(self._properties, dict):
            self._properties = {}
        if not isinstance(self._class_variables, dict):
            self._class_variables = {}
        if not isinstance(self._class_methods, dict):
            self._class_methods = {}
        if not isinstance(self._static_methods, dict):
            self._static_methods = {}

    @property
    def class_variables(self):
        if not isinstance(self._class_variables, dict):
            self._init_class_symbols()
        return self._class_variables.copy()

    @property
    def instance_variables(self):
        if not isinstance(self._instance_variables, dict):
            self._init_class_symbols()
        return self._instance_variables.copy()

    @property
    def properties(self):
        if not isinstance(self._properties, dict):
            self._init_class_symbols()
        return self._properties.copy()

    @property
    def static_methods(self):
        if not isinstance(self._static_methods, dict):
            self._init_class_symbols()
        return self._static_methods.copy()

    @property
    def class_methods(self):
        if not isinstance(self._class_methods, dict):
            self._init_class_symbols()
        return self._class_methods.copy()

    @property
    def instance_methods(self):
        if not isinstance(self._instance_methods, dict):
            self._init_class_symbols()
        return self._instance_methods.copy()

    def constructor_method(self):
        if not isinstance(self._instance_variables, dict):
            self._init_class_symbols()
        if not self._is_init_set:
            self._constructor = (self._instance_methods[constants.INIT_METHOD_ID]
                                 if constants.INIT_METHOD_ID in self._instance_methods
                                 else None)
            self._is_init_set = True
        return self._constructor

    @property
    def abi_type(self) -> AbiType:
        return super().abi_type

    @property
    def stack_item(self) -> StackItemType:
        """
        Get the Neo VM stack item type representation for this type

        :return: the stack item type of this type. Any by default.
        """
        return super().stack_item

    def is_instance_opcodes(self) -> list[tuple[Opcode, bytes]]:
        return [(Opcode.ISTYPE, self.stack_item)]

    def generate_is_instance_type_check(self, code_generator):
        code_generator.insert_type_check(self.stack_item)
