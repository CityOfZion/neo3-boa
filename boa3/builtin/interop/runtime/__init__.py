from typing import Any

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


calling_script_hash: bytes = b''
