from typing import Union

from boa3.builtin import CreateNewEvent, Event
from boa3.builtin.type import ByteString, ECPoint, UInt160

Nep5TransferEvent: Event = CreateNewEvent(
    [
        ('from', bytes),
        ('to', bytes),
        ('amount', int)
    ],
    'transfer'
)
"""
The NEP-5 transfer event that will be triggered whenever a token is transferred, minted or burned. It needs the 
addresses of the sender, receiver and the amount transferred.

:meta hide-value:
"""

Nep11TransferEvent: Event = CreateNewEvent(
    [
        ('from', Union[UInt160, None]),
        ('to', Union[UInt160, None]),
        ('amount', int),
        ('tokenId', ByteString)
    ],
    'Transfer'
)
"""
The NEP-11 Transfer event that will be triggered whenever a token is transferred, minted or burned. It needs the 
addresses of the sender, receiver, amount transferred and the id of the token.

:meta hide-value:
"""


Nep17TransferEvent: Event = CreateNewEvent(
    [
        ('from', Union[UInt160, None]),
        ('to', Union[UInt160, None]),
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


class NeoAccountState:
    """
    Represents the account state of NEO token in the NEO system.

    :ivar balance: the current account balance, which equals to the votes cast
    :vartype balance: int
    :ivar height: the height of the block where the balance changed last time
    :vartype height: int
    :ivar vote_to: the voting target of the account
    :vartype vote_to: ECPoint
    """

    def __init__(self):
        from boa3 import constants
        self.balance: int = 0
        self.height: int = 0
        self.vote_to: ECPoint = ECPoint(bytes(constants.SIZE_OF_ECPOINT))
