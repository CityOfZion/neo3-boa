from typing import Any


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
