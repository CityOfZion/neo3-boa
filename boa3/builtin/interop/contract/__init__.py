from typing import Any, Sequence


def call_contract(script_hash: bytes, method: str, args: Sequence = ()) -> Any:
    """
    Calls a smart contract given the method and the arguments

    :param script_hash: the target smart contract's script hash
    :param method: the name of the method to be executed
    :param args: the specified method's arguments

    :return: the result of the specified method.
    :rtype: Any

    :raise Exception: raised if the script hash is not a valid smart contract or the method was not found or the
        arguments aren't valid to the specified method.
    """
    pass


NEO: bytes = b'\xde\x5f\x57\xd4\x30\xd3\xde\xce\x51\x1c\xf9\x75\xa8\xd3\x78\x48\xcb\x9e\x05\x25'
GAS: bytes = b'\x66\x8e\x0c\x1f\x9d\x7b\x70\xa9\x9d\xd9\xe0\x6e\xad\xd4\xc7\x84\xd6\x41\xaf\xbc'
