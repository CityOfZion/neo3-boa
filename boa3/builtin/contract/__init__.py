from typing import Union

from boa3.builtin import CreateNewEvent
from boa3.builtin.type import UInt160

Nep5TransferEvent = CreateNewEvent(
    [
        ('from_addr', bytes),
        ('to_addr', bytes),
        ('amount', int)
    ],
    'transfer'
)

Nep17TransferEvent = CreateNewEvent(
    [
        ('from_addr', Union[UInt160, None]),
        ('to_addr', Union[UInt160, None]),
        ('amount', int)
    ],
    'Transfer'
)


def abort():
    """
    Abort the execution of a smart contract
    """
    pass
