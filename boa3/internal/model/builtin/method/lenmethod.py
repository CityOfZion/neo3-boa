from collections.abc import Sized
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.icollection import ICollectionType
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class LenMethod(IBuiltinMethod):

    def __init__(self, collection_type: IType = None):
        if not isinstance(collection_type, ICollectionType):
            collection_type = Type.sequence

        identifier = 'len'
        args: dict[str, Variable] = {'__o': Variable(collection_type)}
        super().__init__(identifier, args, return_type=Type.int)

    @property
    def _arg_value(self) -> Variable:
        return self.args['__o']

    @property
    def identifier(self) -> str:
        if self._arg_value.type is Type.str:
            return '-{0}_from_{1}'.format(self._identifier, self._arg_value.type._identifier)
        return self._identifier

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        if not isinstance(params[0], IExpression):
            return False
        return isinstance(params[0].type, SequenceType)

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.SIZE)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self.args['__o'].type):
            return self
        if isinstance(value, Sized) and len(value) == 1:
            value = value[0]

        from boa3.internal.model.builtin.method.lenstrmethod import LenStrMethod
        if Type.str.is_type_of(value):
            return LenStrMethod(value)

        return LenMethod(value)
