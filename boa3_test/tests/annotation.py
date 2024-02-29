from typing import TypeVar

from neo3.core import types

NotificationState = TypeVar('NotificationState', list, tuple)
Notification = tuple[
    types.UInt160,  # contract
    str,  # notification name
    NotificationState  # state
]

Transaction = tuple[
    types.UInt256,  # hash
    int,  # version
    int,  # nonce
    types.UInt160,  # sender
    int,  # system fee
    int,  # network fee
    int,  # valid until block
    bytes,  # script
]
