from typing import Dict, List, Optional, Tuple

from boa3.constants import NEO_SCRIPT
from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetNeoScriptHashMethod(IBuiltinMethod):
    def __init__(self):
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_neo_contract'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=UInt160Type.build())

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        value = NEO_SCRIPT
        return [
            Opcode.get_pushdata_and_data(value)
        ]


class NeoContractProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'NeoContract'
        getter = GetNeoScriptHashMethod()
        super().__init__(identifier, getter)


NeoContract = NeoContractProperty()
