from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.method import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class StorageMapGetMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.model.builtin.interop.storage.storagemap.storagemaptype import _StorageMap
        from boa3.model.type.type import Type
        from boa3.model.type.primitive.bytestringtype import ByteStringType

        identifier = 'get'
        byte_string_type = ByteStringType.build()

        args: Dict[str, Variable] = {'self': Variable(_StorageMap),
                                     'key': Variable(byte_string_type)}

        super().__init__(identifier, args, return_type=Type.bytes)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.interop import Interop
        return [
            (Opcode.SWAP, b''),
            (Opcode.OVER, b''),
            (Opcode.PUSH1, b''),
            (Opcode.PICKITEM, b''),
            (Opcode.SWAP, b''),
            (Opcode.CAT, b''),
            (Opcode.SWAP, b''),
            (Opcode.PUSH0, b''),
            (Opcode.PICKITEM, b''),
        ] + Interop.StorageGet.opcode
