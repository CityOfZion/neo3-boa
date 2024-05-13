from typing import cast, Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken, GasToken
from boa3.sc.runtime import executing_script_hash, notify
from boa3.sc.storage import find, get_uint160, get_context, put_uint160
from boa3.sc.types import UInt160
from boa3.sc.utils import to_int

FEE_RECEIVER_KEY = b'FEE_RECEIVER'

feesMap = get_context().create_map(b'feesMap')


@public
def test_end_while_jump() -> bool:
    iterator = find(b'feesMap')
    fee_receiver = get_uint160(FEE_RECEIVER_KEY)
    while iterator.next():
        token_bytes = cast(bytes, iterator.value[0])
        token_bytes = token_bytes[7:]  # cut 'feesMap' at the beginning of the bytes
        token = cast(UInt160, token_bytes)
        fee_amount = to_int(iterator.value[1])
        if fee_amount > 0:
            notify([token, executing_script_hash, fee_receiver, fee_amount])
    return True


@public
def _deploy(data: Any, update: bool):
    # placeholders for testing
    put_uint160(FEE_RECEIVER_KEY, UInt160())

    feesMap.put(GasToken.hash, 10)
    feesMap.put(NeoToken.hash, 20)
