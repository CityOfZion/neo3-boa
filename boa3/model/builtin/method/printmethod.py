from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class PrintMethod(IBuiltinMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.model.type.type import Type
        identifier = 'print'
        if not isinstance(arg_value, IType):
            arg_value = Type.str

        args: Dict[str, Variable] = {'values': Variable(arg_value)}
        super().__init__(identifier, args, return_type=Type.none)

    @property
    def _arg_values(self) -> Variable:
        return self.args['values']

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
        from boa3.model.type.type import Type
        return (Type.int.is_type_of(self._arg_values.type)
                or Type.bool.is_type_of(self._arg_values.type)
                or Type.str.is_type_of(self._arg_values.type)
                or Type.bytes.is_type_of(self._arg_values.type))

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.interop import Interop
        return Interop.Log.opcode

    @property
    def allow_starred_argument(self) -> bool:
        return True

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        if type(value) == type(self._arg_values.type):
            return self
        return PrintMethod(value)
