import ast
from typing import Any, Dict, List, Optional, Tuple, Union

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ByteArrayMethod(IBuiltinMethod):

    def __init__(self, argument_type: Union[IType, Dict] = None):
        identifier = 'bytearray'
        from boa3.model.type.type import Type

        if isinstance(argument_type, Dict):
            args = argument_type
            defaults = []
        else:
            from boa3.model.type.type import Type
            if argument_type is None or not self.validate_parameters(argument_type):
                argument_type = Type.none

            args: Dict[str, Variable] = {'object': Variable(argument_type)}
            object_default = ast.parse(f"{Type.int.default_value}"
                                       ).body[0].value
            defaults = [object_default]

        super().__init__(identifier, args, defaults=defaults, return_type=Type.bytearray)

    @property
    def _arg_object(self) -> Variable:
        return self.args['object']

    @property
    def identifier(self) -> str:
        from boa3.model.type.type import Type
        if self._arg_object.type is Type.none:
            return self._identifier

        if self._args_on_stack == 2:
            return '-{0}_with_enconding'.format(self._identifier)

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

        if Type.int.is_type_of(param_type):
            return True

        return (isinstance(param_type, SequenceType)
                and (param_type is Type.str
                     or isinstance(param_type.value_type, type(Type.int))
                     ))

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.StackItem import StackItemType
        from boa3.model.type.type import Type

        if self._arg_object.type is Type.int:
            return [(Opcode.NEWBUFFER, b'')]
        else:
            return [(Opcode.CONVERT, StackItemType.Buffer)]

    @property
    def is_supported(self) -> bool:
        # TODO: change when building bytearray from int iterators are implemented
        from boa3.model.type.type import Type
        return self._arg_object.type in (Type.bytes, Type.str, Type.int)

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
            if len(value) == 2:
                from boa3.model.builtin.method.bytearrayencodingmethod import ByteArrayEncodingMethod
                return ByteArrayEncodingMethod()

            value = value[0] if len(value) > 0 else None
        if self.validate_parameters(value):
            return ByteArrayMethod(value)
        return super().build(value)
