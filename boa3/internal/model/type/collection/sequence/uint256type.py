from typing import Any

from boa3.internal import constants
from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.method import Method
from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.bytestype import BytesType
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.AbiType import AbiType


class UInt256Type(BytesType, ClassType):
    """
    A class used to represent Neo's UInt256 type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'UInt256'
        from boa3.internal.model.builtin.method.uint256method import UInt256Method
        self._constructor = UInt256Method(self)

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Hash256

    def constructor_method(self) -> Method | None:
        return self._constructor

    @property
    def default_value(self) -> Any:
        return bytes(constants.SIZE_OF_INT256)

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _UInt256

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, UInt256Type)

    def _init_class_symbols(self):
        super()._init_class_symbols()
        properties = [UInt256ZeroProperty()
                      ]

        for prop in properties:
            self._properties[prop.identifier] = prop

    def is_instance_opcodes(self) -> list[tuple[Opcode, bytes]]:
        from boa3.internal.model.type.classes.pythonclass import PythonClass
        return super(PythonClass, self).is_instance_opcodes()

    def generate_is_instance_type_check(self, code_generator):
        from boa3.internal.model.type.classes.pythonclass import PythonClass
        return super(PythonClass, self).generate_is_instance_type_check(code_generator)

    def _generate_specific_class_type_check(self, code_generator) -> list[int]:
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(constants.SIZE_OF_INT256)
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
        return []

    def _is_instance_inner_opcodes(self, jmp_to_if_false: int = 0) -> list[tuple[Opcode, bytes]]:
        push_int_opcode, size_data = OpcodeHelper.get_push_and_data(constants.SIZE_OF_INT256)

        return [
            (Opcode.SIZE, b''),  # return len(value) == 32
            (push_int_opcode, size_data),
            (Opcode.NUMEQUAL, b'')
        ]


_UInt256 = UInt256Type()


class GetUInt256ZeroMethod(IBuiltinMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = '-uint160_get_zero'
        args = {}
        super().__init__(identifier, args, return_type=Type.int)

    def generate_internal_opcodes(self, code_generator):
        code_generator.convert_literal(_UInt256.default_value)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return


class UInt256ZeroProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'zero'
        getter = GetUInt256ZeroMethod()
        super().__init__(identifier, getter)
