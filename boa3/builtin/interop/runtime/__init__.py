from typing import Any, List

from boa3.builtin.interop.runtime.notification import Notification
from boa3.builtin.interop.runtime.triggertype import TriggerType


def check_witness(hash_or_pubkey: bytes) -> bool:
    """
    Verifies that the transactions or block of the calling contract has validated the required script hash.

    :param hash_or_pubkey: script hash or public key to validate
    :type hash_or_pubkey: bytes
    :return: a boolean value that represents whether the script hash was verified.
    :rtype: bool
    """
    pass


def notify(state: Any):
    """
    Notifies the client from the executing smart contract.

    :param state: the notification message
    """
    pass


def log(message: str):
    """
    Show log messages to the client from the executing smart contract.

    :param message: the log message
    :type message: str
    """
    pass


def trigger() -> TriggerType:
    """
    Verifies if the smart contract trigger is an application trigger.

    :return: a boolean value that represents whether the contract trigger is an application.
    :rtype: TriggerType
    """
    pass


def is_application_trigger() -> bool:
    """
    Verifies if the smart contract trigger is an application trigger.

    :return: a boolean value that represents whether the contract trigger is an application.
    :rtype: bool
    """
    pass


def is_verification_trigger() -> bool:
    """
    Verifies if the smart contract trigger is an verification trigger.

    :return: a boolean value that represents whether the contract trigger is a verification.
    :rtype: bool
    """
    pass


executing_script_hash: bytes = b''
calling_script_hash: bytes = b''
get_time: int = 0
gas_left: int = 0
invocation_counter: int = 0
entry_script_hash: bytes = b''


def get_notifications(script_hash: bytes = bytes(20)) -> List[Notification]:
    """
    This method gets current invocation notifications from specific 'script_hash'

    :param script_hash: must have 20 bytes, but if it's all zero 0000...0000 it refers to all existing notifications
    (like a * wildcard)
    :type script_hash: bytes
    :return: It will return an array of all matched notifications
    :rtype: List[Notification]
    """
    pass
