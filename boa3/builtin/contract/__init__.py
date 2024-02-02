__all__ = [
    'Nep11TransferEvent',
    'Nep17TransferEvent',
    'Nep17Contract',
    'NeoAccountState',
    'abort',
    'to_hex_str',
    'to_script_hash',
]

from typing import Any, Optional, Union

from boa3.builtin.compile_time import CreateNewEvent
from boa3.builtin.contract.Nep17Contract import Nep17Contract
from boa3.builtin.type import ECPoint, UInt160, Event

Nep11TransferEvent: Event = CreateNewEvent(
    [
        ('from', Union[UInt160, None]),
        ('to', Union[UInt160, None]),
        ('amount', int),
        ('tokenId', Union[str, bytes])
    ],
    'Transfer'
)
"""
The NEP-11 Transfer event that should be triggered whenever a non-fungible token is transferred, minted or burned. It 
needs the addresses of the sender, receiver, amount transferred and the id of the token.

Check out the `proposal <https://github.com/neo-project/proposals/blob/master/nep-11.mediawiki>`__ or 
`Neo's Documentation <https://developers.neo.org/docs/n3/develop/write/nep11>`__ about this NEP.

>>> Nep11TransferEvent(b'\\xd1\\x17\\x92\\x82\\x12\\xc6\\xbe\\xfa\\x05\\xa0\\x23\\x07\\xa1\\x12\\x55\\x41\\x06\\x55\\x10\\xe6',  # when calling, it will return None, but the event will be triggered
...                    b'\\x18\\xb7\\x30\\x14\\xdf\\xcb\\xee\\x01\\x30\\x00\\x13\\x9b\\x8d\\xa0\\x13\\xfb\\x96\\xac\\xd1\\xc0', 1, '01')
{
    'name': 'Transfer',
    'script hash': b'\\x13\\xb4\\x51\\xa2\\x1c\\x10\\x12\\xd6\\x13\\x12\\x19\\x0c\\x15\\x61\\x9b\\x1b\\xd1\\xa2\\xf4\\xb2',
    'state': {
        'from': b'\\xd1\\x17\\x92\\x82\\x12\\xc6\\xbe\\xfa\\x05\\xa0\\x23\\x07\\xa1\\x12\\x55\\x41\\x06\\x55\\x10\\xe6',
        'to': b'\\x18\\xb7\\x30\\x14\\xdf\\xcb\\xee\\x01\\x30\\x00\\x13\\x9b\\x8d\\xa0\\x13\\xfb\\x96\\xac\\xd1\\xc0',
        'amount': 1,
        'tokenId': '01'
    }
}

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
The NEP-17 Transfer event that should be triggered whenever a fungible token is transferred, minted or burned. It needs
the addresses of the sender, receiver and the amount transferred.

Check out the `proposal <https://github.com/neo-project/proposals/blob/master/nep-17.mediawiki>`__ or 
`Neo's Documentation <https://developers.neo.org/docs/n3/develop/write/nep17>`__ about this NEP.

>>> Nep17TransferEvent(b'\\xd1\\x17\\x92\\x82\\x12\\xc6\\xbe\\xfa\\x05\\xa0\\x23\\x07\\xa1\\x12\\x55\\x41\\x06\\x55\\x10\\xe6',  # when calling, it will return None, but the event will be triggered
...                    b'\\x18\\xb7\\x30\\x14\\xdf\\xcb\\xee\\x01\\x30\\x00\\x13\\x9b\\x8d\\xa0\\x13\\xfb\\x96\\xac\\xd1\\xc0', 100)
{
    'name': 'Transfer',
    'script hash': b'\\x17\\xe3\\xca\\x91\\xca\\xb7\\xaf\\xdd\\xe6\\xba\\x07\\xaa\\xba\\xa1\\x66\\xab\\xcf\\x00\\x04\\x50',
    'state': {
        'from': b'\\xd1\\x17\\x92\\x82\\x12\\xc6\\xbe\\xfa\\x05\\xa0\\x23\\x07\\xa1\\x12\\x55\\x41\\x06\\x55\\x10\\xe6',
        'to': b'\\x18\\xb7\\x30\\x14\\xdf\\xcb\\xee\\x01\\x30\\x00\\x13\\x9b\\x8d\\xa0\\x13\\xfb\\x96\\xac\\xd1\\xc0',
        'amount': 100
    }
}

:meta hide-value:
"""


def abort(msg: Optional[str] = None):
    """
    Aborts the execution of a smart contract. Using this will cancel the changes made on the blockchain by the
    transaction.

    >>> abort()     # abort doesn't return anything by itself, but the execution will stop and the VMState will be FAULT
    VMState.FAULT

    >>> abort('abort message')
    VMState.FAULT

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
        from boa3.internal import constants
        self.balance: int = 0
        self.height: int = 0
        self.vote_to: ECPoint = ECPoint(bytes(constants.SIZE_OF_ECPOINT))


def to_script_hash(data_bytes: Any) -> bytes:
    """
    Converts a data to a script hash.

    >>> to_script_hash(ECPoint(bytes(range(33))))
    b'\\x12\\xc8z\\xfb3k\\x1e4>\\xb3\\x83\\tK\\xc7\\xdch\\xe5\\xee\\xc7\\x98'

    >>> to_script_hash(b'1234567891')
    b'\\x4b\\x56\\x34\\x17\\xed\\x99\\x7f\\x13\\x22\\x67\\x40\\x79\\x36\\x8b\\xa2\\xcd\\x72\\x41\\x25\\x6d'

    :param data_bytes: data to hash
    :type data_bytes: Any
    :return: the script hash of the data
    :rtype: bytes
    """
    pass


def to_hex_str(data: bytes) -> str:
    """
    Converts bytes into its string hex representation.

    >>> to_hex_str(ECPoint(bytes(range(33))))
    '201f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100'

    >>> to_hex_str(b'1234567891')
    '31393837363534333231'

    :param data: data to represent as hex.
    :type data: bytearray or bytes

    :return: the hex representation of the data
    :rtype: str
    """
    pass
