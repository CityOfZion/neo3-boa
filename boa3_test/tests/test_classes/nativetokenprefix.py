from enum import IntEnum
from typing import Optional, Tuple

from boa3 import constants
from boa3.neo.vm.type.Integer import Integer


def get_native_token_data(token_script: bytes) -> Tuple[Optional[bytes], Optional[int]]:
    prefix: Optional[NativeTokenPrefix] = None
    token_id: NativeTokenId = NativeTokenId.NONE

    if token_script is constants.NEO_SCRIPT:
        prefix = NativeTokenPrefix.NEO
        token_id = NativeTokenId.NEO
    elif token_script is constants.GAS_SCRIPT:
        prefix = NativeTokenPrefix.GAS
        token_id = NativeTokenId.GAS

    return (prefix if prefix is None else Integer(prefix).to_byte_array(min_length=1),
            token_id.value)


class NativeTokenId(IntEnum):
    ContractManagement = -1
    NEO = -3
    GAS = -4

    NONE = 0


class NativeTokenPrefix(IntEnum):
    NEO = 20
    GAS = 20

    NONE = 0
