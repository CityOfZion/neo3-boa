from typing import Any, List, Union

from boa3.builtin.interop.runtime.notification import Notification
from boa3.builtin.interop.runtime.triggertype import TriggerType
from boa3.builtin.type import UInt160


def check_witness(hash_or_pubkey: Union[bytes, UInt160]) -> bool:
    """
    Verifies that the transactions or block of the calling contract has validated the required script hash.

    :param hash_or_pubkey: script hash or public key to validate
    :type hash_or_pubkey: bytes or UInt160
    :return: a boolean value that represents whether the script hash was verified.
    :rtype: bool
    """
    pass


def notify(state: Any, notification_name: str = None):
    """
    Notifies the client from the executing smart contract.

    :param state: the notification message
    :param notification_name: name that'll be linked to the notification
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

    :return: a value that represents the contract trigger type.
    :rtype: TriggerType
    """
    pass


executing_script_hash: UInt160 = UInt160()
calling_script_hash: UInt160 = UInt160()
get_time: int = 0
gas_left: int = 0
get_platform: str = ''
invocation_counter: int = 0
entry_script_hash: UInt160 = UInt160()


def get_notifications(script_hash: UInt160 = UInt160()) -> List[Notification]:
    """
    This method gets current invocation notifications from specific 'script_hash'

    :param script_hash: must have 20 bytes, but if it's all zero 0000...0000 it refers to all existing notifications
    (like a * wildcard)
    :type script_hash: UInt160
    :return: It will return an array of all matched notifications
    :rtype: List[Notification]
    """
    pass
