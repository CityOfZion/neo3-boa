from typing import List

from boa3.builtin import public
from boa3.builtin.interop.crypto import check_multisig_with_ecdsa_secp256r1


@public
def Main():
    pubkeys: List[bytes] = [b'123', b'456']
    assignatures: List[bytes] = [b'098', b'765']
    check_multisig_with_ecdsa_secp256r1(False, pubkeys, assignatures)
