from typing import Dict, List, Tuple

from boa3.model.builtin.interop.contract.contracttype import ContractType
from boa3.model.builtin.interop.nativecontract import ContractManagementMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class CreateMethod(ContractManagementMethod):

    def __init__(self, contract_type: ContractType):
        from boa3.model.type.type import Type
        identifier = 'create_contract'
        syscall = 'deploy'
        args: Dict[str, Variable] = {
            'nef_file': Variable(Type.bytes),
            'manifest': Variable(Type.bytes)
        }

        super().__init__(identifier, syscall, args, return_type=contract_type)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        opcodes = [
            (Opcode.DUP, b''),
            (Opcode.PUSHNULL, b''),
            (Opcode.APPEND, b'')
        ]
        return opcodes + super().opcode
