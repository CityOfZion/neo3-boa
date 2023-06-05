from typing import cast

from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import GAS, NEO
from boa3.builtin.interop.runtime import executing_script_hash, notify
from boa3.builtin.interop.storage import find, get, get_context, put
from boa3.builtin.type import UInt160

FEE_RECEIVER_KEY = b'FEE_RECEIVER'

feesMap = get_context().create_map(b'feesMap')


@public
def test_end_while_jump() -> bool:
    iterator = find(b'feesMap')
    fee_receiver = get(FEE_RECEIVER_KEY)
    while iterator.next():
        token_bytes = cast(bytes, iterator.value[0])
        token_bytes = token_bytes[7:]  # cut 'feesMap' at the beginning of the bytes
        token = cast(UInt160, token_bytes)
        fee_amount = cast(int, iterator.value[1])
        if fee_amount > 0:
            notify([token, executing_script_hash, fee_receiver, fee_amount])
    return True


@public
def deploy() -> bool:
    # placeholders for testing
    put(FEE_RECEIVER_KEY, UInt160())

    feesMap.put(GAS, 10)
    feesMap.put(NEO, 20)
    return True
