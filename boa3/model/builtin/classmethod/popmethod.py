import ast
from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.mapping.mutable.dicttype import DictType
from boa3.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class PopMethod(IBuiltinMethod):
    def __init__(self, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        identifier = 'pop'

        super().__init__(identifier, args, defaults=defaults, return_type=return_type)

    @property
    def identifier(self) -> str:
        from boa3.model.type.type import Type

        if self._arg_self.type is Type.mutableSequence:
            return self._identifier

        if self._arg_self.type is Type.dict:
            return '-{0}_{1}'.format(self._identifier, Type.dict.identifier)

        if Type.mutableSequence.is_type_of(self._arg_self.type):
            return '-{0}_{1}'.format(self._identifier, Type.mutableSequence.identifier)

        return self._identifier

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) < 0 or len(params) > 2:
            return False

        if any(not isinstance(param, (IExpression, IType)) for param in params):
            return False

        sequence_or_map = params[0].type if isinstance(params[0], IExpression) else params[0]
        if not isinstance(sequence_or_map, MutableSequenceType) or not isinstance(sequence_or_map, DictType):
            return False

        if len(params) > 1:
            value = params[1].type if isinstance(params[1], IExpression) else params[1]
            return sequence_or_map.valid_key.is_type_of(value)
        return True

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        return [
            (Opcode.DUP, b''),
            (Opcode.SIGN, b''),
            (Opcode.PUSHM1, b''),
            (Opcode.JMPNE, Integer(5).to_byte_array(min_length=1, signed=True)),
            (Opcode.OVER, b''),
            (Opcode.SIZE, b''),
            (Opcode.ADD, b''),
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b''),
            (Opcode.REVERSE3, b''),
            (Opcode.SWAP, b''),
            (Opcode.REMOVE, b''),
        ]

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and len(value) > 0:
            if len(value) == 2:
                value = value[0]

        from boa3.model.builtin.classmethod.popdictmethod import PopDictMethod
        from boa3.model.builtin.classmethod.popsequencemethod import PopSequenceMethod
        from boa3.model.type.type import Type

        if Type.dict.is_type_of(value):
            return PopDictMethod(value)

        return PopSequenceMethod(value)
