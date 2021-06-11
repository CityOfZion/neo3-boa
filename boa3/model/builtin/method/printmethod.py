from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.collection.sequence.tupletype import TupleType
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class PrintMethod(IBuiltinMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.model.type.type import Type
        identifier = 'print'
        allowed_types = Type.union.build([Type.int, Type.bool, Type.str, Type.bytes])
        if not isinstance(arg_value, IType):
            arg_value = Type.str

        args: Dict[str, Variable] = {}
        vararg = ('values', Variable(arg_value))
        super().__init__(identifier, args, return_type=Type.none, vararg=vararg)
        self._allowed_types = allowed_types

    @property
    def _arg_values(self) -> Variable:
        return self._vararg[1]

    @property
    def identifier(self) -> str:
        from boa3.model.type.type import Type
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
    def is_supported(self) -> bool:
        # TODO: remove when print with sequences and more values are implemented
        return self._allowed_types.is_type_of(self._arg_values.type)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.compiler.codegenerator import get_bytes_count
        from boa3.model.builtin.interop.interop import Interop
        from boa3.neo.vm.type.Integer import Integer

        copy_list_and_reverse = [
            (Opcode.UNPACK, b''),  # copy - it must not change the original
            (Opcode.PACK, b''),
            (Opcode.DUP, b''),
            (Opcode.REVERSEITEMS, b'')
        ]
        check_if_arg_is_empty = [
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),
            (Opcode.PUSH0, b''),
        ]

        complete_loop = (
            [
                (Opcode.DUP, b''),
                (Opcode.POPITEM, b''),
            ] + Interop.Log.opcode +
            check_if_arg_is_empty
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
        return PrintMethod(value)
