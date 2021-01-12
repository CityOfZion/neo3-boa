from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ByteArrayMethod(IBuiltinMethod):

    def __init__(self, argument_type: IType = None):
        from boa3.model.type.type import Type
        if argument_type is None or not self.validate_parameters(argument_type):
            argument_type = Type.none

        identifier = 'bytearray'
        args: Dict[str, Variable] = {'object': Variable(argument_type)}
        super().__init__(identifier, args, return_type=Type.bytearray)

    @property
    def _arg_object(self) -> Variable:
        return self.args['object']

    @property
    def identifier(self) -> str:
        from boa3.model.type.type import Type
        if self._arg_object.type is Type.none:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self._arg_object.type._identifier)

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) > 1:
            return False
        if len(params) == 0:
            return True

        from boa3.model.type.itype import IType
        if not isinstance(params[0], (IExpression, IType)):
            return False

        param_type: IType = params[0].type if isinstance(params[0], IExpression) else params[0]
        from boa3.model.type.type import Type
        # TODO: change when building bytearray given size is implemented
        return (isinstance(param_type, SequenceType)
                and (param_type is Type.str
                     or isinstance(param_type.value_type, type(Type.int))
                     ))

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return []

    @property
    def is_supported(self) -> bool:
        # TODO: change when building bytearray from string and int iterators are implemented
        from boa3.model.type.type import Type
        return self._arg_object.type is Type.bytes

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self._arg_object.type):
            return self
        if isinstance(value, list):
            value = value[0] if len(value) > 0 else None
        if self.validate_parameters(value):
            return ByteArrayMethod(value)
        return super().build(value)
