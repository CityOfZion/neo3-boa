from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.mapping.mappingtype import MappingType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class MapKeysMethod(IBuiltinMethod):
    def __init__(self, mapping_type: MappingType = None):
        from boa3.model.type.type import Type
        if not isinstance(mapping_type, MappingType):
            self_arg = Variable(Type.mapping)
            return_type = Type.sequence
        else:
            self_arg = Variable(mapping_type)
            return_type = Type.sequence.build_collection(mapping_type.key_type)

        identifier = 'keys'
        args: Dict[str, Variable] = {'self': self_arg}
        super().__init__(identifier, args, return_type=return_type)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1 or not isinstance(params[0], IExpression):
            return False
        return self._arg_self.type.is_type_of(params[0].type)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.KEYS, b'')]

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self.args['self'].type):
            return self
        if isinstance(value, MappingType):
            return MapKeysMethod(value)
        return super().build(value)
