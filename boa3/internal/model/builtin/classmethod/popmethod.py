import ast
from typing import Any, Dict, List, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.mapping.mutable.dicttype import DictType
from boa3.internal.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PopMethod(IBuiltinMethod):
    def __init__(self, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        identifier = 'pop'

        super().__init__(identifier, args, defaults=defaults, return_type=return_type)

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type

        if self._arg_self.type is Type.mutableSequence:
            return self._identifier

        if Type.dict.is_type_of(self._arg_self.type):

            if len(self.args) == 2:
                return '-{0}_{1}'.format(self._identifier, Type.dict.identifier)

            elif len(self.args) == 3:
                return '-{0}_{1}_{2}'.format(self._identifier, Type.dict.identifier, 'default')

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

    def generate_internal_opcodes(self, code_generator):
        # get the item from the sequence/dict
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)

        # remove the item from the sequence/dict
        code_generator.swap_reverse_stack_items(3)
        code_generator.swap_reverse_stack_items(2)
        code_generator.insert_opcode(Opcode.REMOVE)

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, list):
            value = [value]

        from boa3.internal.model.builtin.classmethod.popdictmethod import PopDictMethod
        from boa3.internal.model.builtin.classmethod.popsequencemethod import PopSequenceMethod
        from boa3.internal.model.type.type import Type

        if Type.dict.is_type_of(value[0]):
            if len(value) == 3:
                from boa3.internal.model.builtin.classmethod.popdictdefaultmethod import PopDictDefaultMethod
                return PopDictDefaultMethod(value[0])
            return PopDictMethod(value[0])

        return PopSequenceMethod(value[0])
