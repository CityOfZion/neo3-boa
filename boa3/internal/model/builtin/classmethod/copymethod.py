from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.mutable.listtype import ListType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class CopyMethod(IBuiltinMethod):
    def __init__(self, arg_value: IType | None = None):
        from boa3.internal.model.type.type import Type
        identifier = 'copy'

        self._allowed_types = [Type.dict, Type.list]
        default_type = Type.list
        if not self._is_valid_type(arg_value):
            arg_value = default_type

        args: dict[str, Variable] = {'self': Variable(arg_value)}
        super().__init__(identifier, args, return_type=arg_value)

    def _is_valid_type(self, arg_type: IType | None) -> bool:
        return (isinstance(arg_type, IType) and
                any(allowed_type.is_type_of(arg_type) for allowed_type in self._allowed_types))

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self._arg_self.type is Type.list:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self._arg_self.type._identifier)

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        return isinstance(params[0], IExpression) and isinstance(params[0].type, ListType)

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.UNPACK)
        code_generator.insert_opcode(Opcode.PACK)

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        if value == self.args['self']:
            return self

        from boa3.internal.model.builtin.classmethod.copydictmethod import CopyDictMethod
        from boa3.internal.model.builtin.classmethod.copylistmethod import CopyListMethod
        from boa3.internal.model.type.type import Type

        if Type.dict.is_type_of(value):
            return CopyDictMethod(value)

        return CopyListMethod(value)
