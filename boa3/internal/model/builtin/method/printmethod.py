from typing import Any, Dict, List, Optional, Tuple

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.collection.sequence.tupletype import TupleType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PrintMethod(IBuiltinMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type
        identifier = 'print'
        if not isinstance(arg_value, IType):
            arg_value = Type.str

        args: Dict[str, Variable] = {}
        vararg = ('values', Variable(arg_value))
        super().__init__(identifier, args, return_type=Type.none, vararg=vararg)

        self._print_value_opcodes = None

    @property
    def _arg_values(self) -> Variable:
        return self._vararg[1]

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self._arg_values.type is Type.str:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self._arg_values.type._identifier)

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        if not isinstance(params[0], IExpression):
            return False
        return isinstance(params[0].type, SequenceType)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.compiler.codegenerator import get_bytes_count
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.neo.vm.type.Integer import Integer

        check_if_arg_is_empty = [
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),
            (Opcode.PUSH0, b''),
        ]
        copy_list_and_reverse = [
            (Opcode.UNPACK, b''),  # copy - it must not change the original
            (Opcode.PACK, b''),
            (Opcode.DUP, b''),
            (Opcode.REVERSEITEMS, b'')
        ]

        complete_loop = (
            [
                (Opcode.DUP, b''),
                (Opcode.POPITEM, b''),
            ] + self.print_value_opcodes
            + Interop.Log.opcode
            + check_if_arg_is_empty
        )
        complete_loop.append((Opcode.JMPNE, Integer(-get_bytes_count(complete_loop)).to_byte_array(signed=True)))

        return (check_if_arg_is_empty +
                [
                    (Opcode.JMPEQ, Integer(get_bytes_count(copy_list_and_reverse)
                                           + 1  # the size of the JMPEQ arg
                                           + get_bytes_count(complete_loop)).to_byte_array(signed=True)),
                ] +
                copy_list_and_reverse +
                complete_loop +
                [
                    (Opcode.DROP, b'')
                ])

    @property
    def print_value_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        if self._print_value_opcodes is None:
            self._print_value_opcodes = []

        return self._print_value_opcodes

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        if isinstance(value, TupleType):
            value = value.value_type
        if type(value) == type(self._arg_values.type):
            return self

        from boa3.internal.model.builtin.method.printbytestringmethod import PrintByteStringMethod
        from boa3.internal.model.type.classes.userclass import UserClass
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.primitive.bytestringtype import ByteStringType

        if Type.bool.is_type_of(value):
            from boa3.internal.model.builtin.method.printboolmethod import PrintBoolMethod
            return PrintBoolMethod()

        elif Type.int.is_type_of(value):
            from boa3.internal.model.builtin.method.printintmethod import PrintIntMethod
            return PrintIntMethod()

        elif ByteStringType.build().is_type_of(value):
            return PrintByteStringMethod(value)

        elif isinstance(value, UserClass):
            from boa3.internal.model.builtin.method.printclassmethod import PrintClassMethod
            return PrintClassMethod(value)

        elif Type.sequence.is_type_of(value):
            from boa3.internal.model.builtin.method.printsequencemethod import PrintSequenceMethod
            return PrintSequenceMethod(value)

        return PrintByteStringMethod(value)
