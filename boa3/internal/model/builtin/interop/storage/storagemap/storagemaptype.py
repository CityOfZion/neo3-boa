from typing import Any, Self

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property
from boa3.internal.model.type.classes.classarraytype import ClassArrayType
from boa3.internal.model.variable import Variable


class StorageMapType(ClassArrayType):
    """
    A class used to represent Neo StorageMap class
    """

    def __init__(self):
        super().__init__('StorageMap')

        self._variables: dict[str, Variable] = {}
        self._constructor: Method = None
        self._instance_methods: dict[str, Method] = {}

    @property
    def instance_variables(self) -> dict[str, Variable]:
        return self._variables.copy()

    @property
    def class_variables(self) -> dict[str, Variable]:
        return {}

    @property
    def _all_variables(self) -> dict[str, Variable]:
        from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import \
            _StorageContext as StorageContextType
        from boa3.internal.model.type.type import Type

        private_variables = {
            '_context': Variable(StorageContextType),
            '_prefix': Variable(Type.bytes)
        }
        variables = super()._all_variables
        variables.update(private_variables)
        return variables

    @property
    def properties(self) -> dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> dict[str, Method]:
        # avoid recursive import
        if len(self._instance_methods) == 0:
            from boa3.internal.model.builtin.interop.storage.storagemap.storagemapdeletemethod import StorageMapDeleteMethod
            from boa3.internal.model.builtin.interop.storage.storagemap.storagemapgetmethod import StorageMapGetMethod
            from boa3.internal.model.builtin.interop.storage.storagemap.storagemapputmethod import StorageMapPutMethod

            self._instance_methods = {
                'get': StorageMapGetMethod(),
                'put': StorageMapPutMethod(),
                'delete': StorageMapDeleteMethod()
            }
        return self._instance_methods

    def constructor_method(self) -> Method | None:
        # was having a problem with recursive import
        if self._constructor is None:
            self._constructor: Method = StorageMapMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _StorageMap

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, StorageMapType)


_StorageMap = StorageMapType()


class StorageMapMethod(IBuiltinMethod):

    def __init__(self, return_type: StorageMapType):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.builtin.interop.storage.storagecontext.storagecontexttype import \
            _StorageContext as StorageContextType

        identifier = '-StorageMap__init__'
        args: dict[str, Variable] = {
            'context': Variable(StorageContextType),
            'prefix': Variable(Type.bytes)
        }
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    def generate_internal_opcodes(self, code_generator):
        code_generator.convert_new_array(len(self.args), self.return_type)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return
