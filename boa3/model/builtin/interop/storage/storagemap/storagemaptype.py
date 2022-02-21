from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classes.classarraytype import ClassArrayType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class StorageMapType(ClassArrayType):
    """
    A class used to represent Neo StorageMap class
    """

    def __init__(self):
        super().__init__('StorageMap')

        self._variables: Dict[str, Variable] = {}
        self._constructor: Method = None
        self._instance_methods: Dict[str, Method] = {}

    @property
    def instance_variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def class_variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def _all_variables(self) -> Dict[str, Variable]:
        from boa3.model.builtin.interop.storage.storagecontext.storagecontexttype import \
            _StorageContext as StorageContextType
        from boa3.model.type.primitive.bytestringtype import ByteStringType

        byte_string_type = ByteStringType.build()
        private_variables = {
            '_context': Variable(StorageContextType),
            '_prefix': Variable(byte_string_type)
        }
        variables = super()._all_variables
        variables.update(private_variables)
        return variables

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> Dict[str, Method]:
        # avoid recursive import
        if len(self._instance_methods) == 0:
            from boa3.model.builtin.interop.storage.storagemap.storagemapdeletemethod import StorageMapDeleteMethod
            from boa3.model.builtin.interop.storage.storagemap.storagemapgetmethod import StorageMapGetMethod
            from boa3.model.builtin.interop.storage.storagemap.storagemapputmethod import StorageMapPutMethod

            self._instance_methods = {
                'get': StorageMapGetMethod(),
                'put': StorageMapPutMethod(),
                'delete': StorageMapDeleteMethod()
            }
        return self._instance_methods

    def constructor_method(self) -> Optional[Method]:
        # was having a problem with recursive import
        if self._constructor is None:
            self._constructor: Method = StorageMapMethod(self)
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> StorageMapType:
        if value is None or cls._is_type_of(value):
            return _StorageMap

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, StorageMapType)


_StorageMap = StorageMapType()


class StorageMapMethod(IBuiltinMethod):

    def __init__(self, return_type: StorageMapType):
        from boa3.model.type.type import Type
        from boa3.model.builtin.interop.storage.storagecontext.storagecontexttype import \
            _StorageContext as StorageContextType

        identifier = '-StorageMap__init__'
        args: Dict[str, Variable] = {
            'context': Variable(StorageContextType),
            'prefix': Variable(Type.union.build([Type.bytes,
                                                 Type.str
                                                 ]))
        }
        super().__init__(identifier, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [
            (Opcode.PUSH2, b''),
            (Opcode.PACK, b'')
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
