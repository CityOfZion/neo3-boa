from typing import Any, List, Union

from boa3.builtin.interop.runtime.notification import Notification
from boa3.builtin.interop.runtime.triggertype import TriggerType
from boa3.builtin.type import ECPoint, UInt160


def check_witness(hash_or_pubkey: Union[UInt160, ECPoint]) -> bool:
    """
    Verifies that the transactions or block of the calling contract has validated the required script hash.

    :param hash_or_pubkey: script hash or public key to validate
    :type hash_or_pubkey: UInt160 or ECPoint
    :return: a boolean value that represents whether the script hash was verified
    :rtype: bool
    """
    pass


def notify(state: Any, notification_name: str = None):
    """
    Notifies the client from the executing smart contract.

    :param state: the notification message
    :type state: Any
    :param notification_name: name that'll be linked to the notification
    :type notification_name: str
    """
    pass


def log(message: str):
    """
    Show log messages to the client from the executing smart contract.

    :param message: the log message
    :type message: str
    """
    pass


def get_trigger() -> TriggerType:
    """
    Return the smart contract trigger type.

    :return: a value that represents the contract trigger type
    :rtype: TriggerType
    """
    pass


def get_notifications(script_hash: UInt160 = UInt160()) -> List[Notification]:
    """
    This method gets current invocation notifications from specific 'script_hash'.

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

    :return: the magic number of the current network
    :rtype: int
    """
    pass


def burn_gas(gas: int):
    """
    Burns GAS to benefit the NEO ecosystem.

    :param gas: the amount of GAS that will be burned
    :type gas: int

    :raise Exception: raised if gas value is negative.
    """
    pass


def get_random() -> int:
    """
    Gets the next random number.

    :return: the next random number
    :rtype: int
    """
    pass


address_version: int = 0
"""
Gets the address version of the current network.

:meta hide-value:
"""


executing_script_hash: UInt160 = UInt160()
"""
Gets the script hash of the current context.

:meta hide-value:
"""

calling_script_hash: UInt160 = UInt160()
"""
Gets the script hash of the calling contract.

:meta hide-value:
"""

time: int = 0
"""
Gets the timestamp of the current block.

:meta hide-value:
"""

gas_left: int = 0
"""
Gets the remaining GAS that can be spent in order to complete the execution.

:meta hide-value:
"""

platform: str = ''
"""
Gets the name of the current platform.

:meta hide-value:
"""

invocation_counter: int = 0
"""
Gets the number of times the current contract has been called during the execution.

:meta hide-value:
"""

entry_script_hash: UInt160 = UInt160()
"""
Gets the script hash of the entry context.

:meta hide-value:
"""

script_container: Any = None
"""
Gets the current script container.

:meta hide-value:
"""
