from typing import Any, cast, Union

from boa3.builtin.compile_time import public
from boa3.builtin.interop import runtime
from boa3.builtin.type import UInt160
from boa3.builtin.type.helper import to_str

TEST_AMOUNT_1 = 10
TEST_AMOUNT_2 = 2


@public
def main(from_address: Union[UInt160, None], amount: int, data: Any):
    if from_address is None:
        return
    from_address = cast(UInt160, from_address)

    if runtime.calling_script_hash == runtime.executing_script_hash:
        corresponding_amount = amount * TEST_AMOUNT_1
        mint(from_address, corresponding_amount)   # typing failed here
    else:
        corresponding_amount = amount * TEST_AMOUNT_2
        mint(from_address, corresponding_amount)   # typing failed here


def mint(account: UInt160, amount: int):
    assert amount >= 0
    if amount != 0:
        runtime.log(to_str(account))
