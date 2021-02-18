from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class StorageContextCreateMapMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.model.builtin.interop.storage.storagecontext.storagecontexttype import _StorageContext
        from boa3.model.builtin.interop.storage.storagemap.storagemaptype import _StorageMap
        from boa3.model.type.type import Type

        identifier = 'create_map'
        args: Dict[str, Variable] = {'self': Variable(_StorageContext),
                                     'prefix': Variable(Type.union.build([Type.bytes,
                                                                          Type.str
                                                                          ]))}

        super().__init__(identifier, args, return_type=_StorageMap)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.storage.storagemap.storagemaptype import _StorageMap as StorageMapType
        return StorageMapType.constructor_method().opcode
