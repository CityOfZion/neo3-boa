from enum import IntEnum
from typing import Optional, Tuple

from boa3.internal import constants
from boa3.internal.neo.vm.type.Integer import Integer


def get_native_contract_data(token_script: bytes) -> Tuple[Optional[bytes], Optional[int]]:
    prefix: Optional[NativeContractPrefix] = None
    contract_id: NativeContractId = NativeContractId.NONE

    if token_script is constants.NEO_SCRIPT:
        prefix = NativeContractPrefix.NEO
        contract_id = NativeContractId.NEO
    elif token_script is constants.GAS_SCRIPT:
        prefix = NativeContractPrefix.GAS
        contract_id = NativeContractId.GAS
    elif token_script is constants.MANAGEMENT_SCRIPT:
        prefix = NativeContractPrefix.ContractManagement
        contract_id = NativeContractId.ContractManagement

    return (prefix if prefix is None else Integer(prefix).to_byte_array(min_length=1),
            contract_id.value)


class NativeContractId(IntEnum):
    ContractManagement = -1
    NEO = -5
    GAS = -6
    Oracle = -9

    NONE = 0


class NativeContractPrefix(IntEnum):
    ContractManagement = 8
    NEO = 20
    GAS = 20

    NONE = 0
