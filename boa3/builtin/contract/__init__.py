from typing import Union

from boa3.builtin import CreateNewEvent, Event
from boa3.builtin.type import UInt160

Nep5TransferEvent: Event = CreateNewEvent(
    [
        ('from_addr', bytes),
        ('to_addr', bytes),
        ('amount', int)
    ],
    'transfer'
)
"""
The NEP-5 transfer event that will be triggered whenever a token is transferred, minted or burned. It needs the 
addresses of the sender, receiver and the amount transferred.

:meta hide-value:
"""

Nep17TransferEvent: Event = CreateNewEvent(
    [
        ('from_addr', Union[UInt160, None]),
        ('to_addr', Union[UInt160, None]),
        ('amount', int)
    ],
    'Transfer'
)
"""
The NEP-17 Transfer event that will be triggered whenever a token is transferred, minted or burned. It needs the 
addresses of the sender, receiver and the amount transferred.

:meta hide-value:
"""


def abort():
    """
    Aborts the execution of a smart contract.
    """
    pass
