from typing import List

from boa3.builtin import public
from boa3.builtin.interop.crypto import check_multisig
from boa3.builtin.type import ECPoint


@public
def Main():
    pubkeys: List[ECPoint] = [ECPoint(b'123456789012345678901234567890123'),
                              ECPoint(b'abcdefghijklmnopqrstuvwxyz1234567')]
    assignatures: List[bytes] = [b'098', b'765']
    check_multisig(pubkeys, assignatures)
