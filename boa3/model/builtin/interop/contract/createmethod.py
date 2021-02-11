from typing import Dict, List, Tuple

from boa3.model.builtin.interop.contract.contractmanagementmethod import ContractManagementMethod
from boa3.model.builtin.interop.contract.contracttype import ContractType
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
        from boa3.model.builtin.interop.interop import Interop
        from boa3.neo.vm.type.Integer import Integer
        from boa3.neo.vm.type.String import String

        method = String(self._sys_call).to_bytes()
        opcodes = [
            (Opcode.DUP, b''),
            (Opcode.PUSHNULL, b''),
            (Opcode.APPEND, b''),
            (Opcode.PUSHDATA1, Integer(len(method)).to_byte_array(min_length=1) + method)
        ]
        return (opcodes
                + Interop.ManagementContractScriptHash.getter.opcode
                + Interop.CallContract.opcode
                )
