import ast
from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ListMethod(IBuiltinMethod):

    def __init__(self, args: Dict[str, Variable] = None, return_type=None, defaults: List[ast.AST] = None):
        identifier = 'list'

        self._prepare_for_packing = None

        super().__init__(identifier, args, defaults=defaults, return_type=return_type)

    @property
    def _arg_value(self) -> Variable:
        return self.args['value']

    @property
    def identifier(self) -> str:
        from boa3.model.type.type import Type

        if self._arg_value.type is Type.str or self._arg_value.type is Type.bytes:
            return '-{0}_{1}'.format(self._identifier, Type.str.identifier + Type.bytes.identifier)

        if Type.sequence.is_type_of(self._arg_value.type):
            return '-{0}_{1}'.format(self._identifier, Type.sequence.identifier)

        if Type.mapping.is_type_of(self._arg_value.type):
            return '-{0}_{1}'.format(self._identifier, Type.mapping.identifier)

        return self._identifier

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:

        pack_values = [(Opcode.PACK, b'')]

        return self.prepare_for_packing + pack_values

    @property
    def prepare_for_packing(self) -> List[Tuple[Opcode, bytes]]:

        if self._prepare_for_packing is None:
            self._prepare_for_packing = []

        return self._prepare_for_packing

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, list):
            value = [value]

        from boa3.model.type.type import Type

        from boa3.model.type.annotation.uniontype import UnionType
        is_union = len(value) > 0 and isinstance(value[0], UnionType)
        union_types = value[0].union_types if is_union else None

        if len(value) > 0:
            if Type.str.is_type_of(value[0]) or Type.bytes.is_type_of(value[0]) or \
                    (is_union and all((union_type is Type.str or union_type is Type.bytes) for union_type in union_types)):
                from boa3.model.builtin.method import ListBytesStringMethod
                return ListBytesStringMethod(value[0])

            if Type.mapping.is_type_of(value[0]):
                from boa3.model.builtin.method import ListMappingMethod
                return ListMappingMethod(value[0])

            if is_union and \
                    any((union_type is Type.str or
                         union_type is Type.bytes or
                         Type.sequence.is_type_of(union_type) or
                         Type.mapping.is_type_of(union_type)) for union_type in union_types):
                from boa3.model.builtin.method import ListGenericMethod
                return ListGenericMethod(value[0])

            if value[0] is Type.any:
                from boa3.model.builtin.method import ListGenericMethod
                return ListGenericMethod()

            if Type.sequence.is_type_of(value[0]):
                from boa3.model.builtin.method import ListSequenceMethod
                return ListSequenceMethod(value[0])
