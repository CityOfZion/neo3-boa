__all__ = [
    'Notification',
    'TriggerType',
    'check_witness',
    'notify',
    'log',
    'get_trigger',
    'get_notifications',
    'get_network',
    'burn_gas',
    'get_random',
    'load_script',
    'address_version',
    'executing_script_hash',
    'calling_script_hash',
    'time',
    'gas_left',
    'platform',
    'invocation_counter',
    'entry_script_hash',
    'script_container',
]


from typing import Any, List, Union, Sequence

from boa3.builtin.interop.contract.callflagstype import CallFlags
from boa3.builtin.interop.runtime.notification import Notification
from boa3.builtin.interop.runtime.triggertype import TriggerType
from boa3.builtin.type import ECPoint, UInt160


def check_witness(hash_or_pubkey: Union[UInt160, ECPoint]) -> bool:
    """
    Verifies that the transactions or block of the calling contract has validated the required script hash.

    >>> check_witness(calling_script_hash)
    True

    >>> check_witness(UInt160(bytes(20)))
    False

    :param hash_or_pubkey: script hash or public key to validate
    :type hash_or_pubkey: UInt160 or ECPoint
    :return: a boolean value that represents whether the script hash was verified
    :rtype: bool
    """
    pass


def notify(state: Any, notification_name: str = None):
    """
    Notifies the client from the executing smart contract.

    >>> var = 10
    ... notify(var)     # An event will be triggered
    None

    >>> var = 10
    ... notify(var, 'custom event name')     # An event will be triggered
    None

    :param state: the notification message
    :type state: Any
    :param notification_name: name that'll be linked to the notification
    :type notification_name: str
    """
    pass


def log(message: str):
    """
    Show log messages to the client from the executing smart contract.

    >>> log('log sent')     # An event that can be shown on the CLI
    log sent

    :param message: the log message
    :type message: str
    """
    pass


def get_trigger() -> TriggerType:
    """
    Return the smart contract trigger type.

    >>> get_trigger()
    TriggerType.APPLICATION

    :return: a value that represents the contract trigger type
    :rtype: TriggerType
    """
    pass


def get_notifications(script_hash: UInt160 = UInt160()) -> List[Notification]:
    """
    This method gets current invocation notifications from specific 'script_hash'.

    >>> notify(1); notify(2); notify(3)
    ... get_notifications(UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2'))
    [
        [
            b'8\\xfe\\x11\\n\\xff7J\\xb8}\\xe9x6@\\xea\\x0b\\x00\\xf1|\\x82v',
            'notify',
            [1]
        ],
        [
            b'8\\xfe\\x11\\n\\xff7J\\xb8}\\xe9x6@\\xea\\x0b\\x00\\xf1|\\x82v',
            'notify',
            [2]
        ],
        [
            b'8\\xfe\\x11\\n\\xff7J\\xb8}\\xe9x6@\\xea\\x0b\\x00\\xf1|\\x82v',
            'notify',
            [3]
        ]
    ]

    :param script_hash: must have 20 bytes, but if it's all zero 0000...0000 it refers to all existing notifications
        (like a * wildcard)
    :type script_hash: UInt160
    :return: It will return an array of all matched notifications
    :rtype: List[Notification]
    """
    pass


def get_network() -> int:
    """
    Gets the magic number of the current network.

    >>> get_network()
    860243278

    :return: the magic number of the current network
    :rtype: int
    """
    pass


def burn_gas(gas: int):
    """
    Burns GAS to benefit the NEO ecosystem.

    >>> burn_gas(1000)
    None

    :param gas: the amount of GAS that will be burned
    :type gas: int

    :raise Exception: raised if gas value is negative.
    """
    pass


def get_random() -> int:
    """
    Gets the next random number.

    >>> get_random()
    191320526825634396960813166838892720709

    >>> get_random()
    99083669484001682562631729023191545809

    >>> get_random()
    328056213623902365838800581788496514419

    :return: the next random number
    :rtype: int
    """
    pass


def load_script(script: bytes, args: Sequence = (), flags: CallFlags = CallFlags.NONE) -> Any:
    """
    Loads a script at runtime.

    >>> from typing import cast
    ... from boa3.builtin.vm import Opcode
    ... cast(int, load_script(Opcode.ADD, [10, 2]))
    12

    """
    pass


address_version: int = 0
"""
Gets the address version of the current network.

>>> address_version
53

:meta hide-value:
"""


executing_script_hash: UInt160 = UInt160()
"""
Gets the script hash of the current context.

>>> executing_script_hash
b'^b]\\x90#\\xbf\\xcc\\x1f\\xd8\\x9e\\xe3\\xa4zd\\x14\\xa4\\xf0\\x96\\x9f`'

:meta hide-value:
"""

calling_script_hash: UInt160 = UInt160()
"""
Gets the script hash of the calling contract.

>>> calling_script_hash
b'\\x05\\x7f\\xc2\\x9d\\xba\\xb2\\xc1x\\xf5\\x81\\x83\\xbf\\xcb\\x87/\\xc3!\\xca\\xe1\\xd0'

:meta hide-value:
"""

time: int = 0
"""
Gets the timestamp of the current block.

>>> time
1685395697108

:meta hide-value:
"""

gas_left: int = 0
"""
Gets the remaining GAS that can be spent in order to complete the execution.

>>> gas_left
1999015490

:meta hide-value:
"""

platform: str = ''
"""
Gets the name of the current platform.

>>> platform
'NEO'

:meta hide-value:
"""

invocation_counter: int = 0
"""
Gets the number of times the current contract has been called during the execution.

>>> invocation_counter
1

:meta hide-value:
"""

entry_script_hash: UInt160 = UInt160()
"""
Gets the script hash of the entry context.

>>> entry_script_hash
b'\\tK\\xb31\\xa8\\x13\\x80`\\xad\\xf6\\xda\\xdf\\xc6R\\x9b\\xfdB\\xbf\\x83\\x8f'

:meta hide-value:
"""

script_container: Any = None
"""
Gets the current script container.

>>> script_container
[
    b'\\xf1y\\xc2\\xd6\\x1c\\xb6\\x98\\xa4\\xdc\\xf3\\xd67s\\xd7E\\xf0<;\\x98+\\xa2T\\x03P,T\\xe8\\xc6{ \\x101', 
    0, 
    442907905, 
    '\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00', 
    0, 
    0, 
    0, 
    ''
]

>>> script_container
[
    b"S{\\xed'\\x85&\\xf5\\x93U=\\xc1\\xbf'\\x95\\xc4/\\x80X\\xdb\\xd5\\xa1-\\x97q\\x85\\xe3I\\xe5\\x99cd\\x04",
    0,
    '\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00',
    '\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00',
    1468595301000,
    2083236893,
    0,
    0,
    b'\\xa6\\xea\\xb0\\xae\\xaf\\xb4\\x96\\xa1\\x1b\\xb0|\\x88\\x17\\xcar\\xa5J\\x00\\x12\\x04',
    0,
]

:meta hide-value:
"""
