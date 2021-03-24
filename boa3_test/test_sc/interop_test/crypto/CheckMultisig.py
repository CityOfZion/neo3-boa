from typing import List

from boa3.builtin import public
from boa3.builtin.interop.crypto import check_multisig


@public
def Main():
    pubkeys: List[bytes] = [b'123', b'456']
    assignatures: List[bytes] = [b'098', b'765']
    check_multisig(pubkeys, assignatures)
