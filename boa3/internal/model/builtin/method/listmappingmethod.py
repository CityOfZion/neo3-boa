from typing import Dict, List, Tuple

from boa3.internal.model.builtin.method.listmethod import ListMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ListMappingMethod(ListMethod):

    def __init__(self, mapping_type: IType = None):
        from boa3.internal.model.type.type import Type
        if mapping_type is None:
            mapping_type = Type.mapping

        args: Dict[str, Variable] = {
            'value': Variable(mapping_type),
        }

        return_type = Type.list.build_collection(mapping_type.key_type)

        super().__init__(args, return_type)

    @property
    def prepare_for_packing(self) -> List[Tuple[Opcode, bytes]]:

        if self._prepare_for_packing is None:

            self._prepare_for_packing = [
                (Opcode.KEYS, b''),
                (Opcode.UNPACK, b'')
            ]

        return super().prepare_for_packing
