from typing import Any, List, Optional, Tuple

from boa3 import constants
from boa3.model.method import Method
from boa3.model.type.itype import IType
from boa3.model.type.primitive.bytestype import BytesType
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.AbiType import AbiType


class ECPointType(BytesType):
    """
    A class used to represent Neo's UInt160 type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'ECPoint'
        from boa3.model.builtin.method.ecpointmethod import ECPointMethod
        self._constructor = ECPointMethod(self)

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def abi_type(self) -> AbiType:
        return AbiType.PublicKey

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @property
    def default_value(self) -> Any:
        return bytes(constants.SIZE_OF_ECPOINT)

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _ECPoint

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, ECPointType)

    def _init_class_symbols(self):
        super()._init_class_symbols()

        from boa3.model.builtin.builtin import Builtin

        instance_methods = [Builtin.ScriptHash,
                            ]

        for instance_method in instance_methods:
            self._instance_methods[instance_method.raw_identifier] = instance_method.build(self)

    def is_instance_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.type.classes.pythonclass import PythonClass
        return super(PythonClass, self).is_instance_opcodes()

    def _is_instance_inner_opcodes(self, jmp_to_if_false: int = 0) -> List[Tuple[Opcode, bytes]]:
        from boa3 import constants
        push_int_opcode, size_data = Opcode.get_push_and_data(constants.SIZE_OF_ECPOINT)

        return [
            (Opcode.SIZE, b''),  # return len(value) == 33
            (push_int_opcode, size_data),
            (Opcode.NUMEQUAL, b'')
        ]


_ECPoint = ECPointType()
