from typing import Any, Sequence

from boa3.builtin.interop.contract.contract import Contract
from boa3.builtin.type import UInt160


def call_contract(script_hash: UInt160, method: str, args: Sequence = ()) -> Any:
    """
    Calls a smart contract given the method and the arguments

    :param script_hash: the target smart contract's script hash
    :type script_hash: UInt160
    :param method: the name of the method to be executed
    :type method: str
    :param args: the specified method's arguments
    :type args: Sequence[Any]

    :return: the result of the specified method.
    :rtype: Any

    :raise Exception: raised if the script hash is not a valid smart contract or the method was not found or the
        arguments aren't valid to the specified method.
    """
    pass


def create_contract(nef_file: bytes, manifest: bytes) -> Contract:
    """
    Creates a smart contract given the script and the manifest

    :param nef_file: the target smart contract's compiled nef
    :type nef_file: bytes
    :param manifest: the manifest.json that describes how the script should behave
    type manifest: bytes
    :return: the contract that was created.
    :rtype: Any

    :raise Exception: raised if the nef or the manifest are not a valid smart contract.
    """
    pass


def update_contract(nef_file: bytes, manifest: bytes):
    """
    Updates the executing smart contract given the script and the manifest

    :param nef_file: the new smart contract's compiled nef
    :type nef_file: bytes
    :param manifest: the new smart contract's manifest
    :type manifest: bytes

    :raise Exception: raised if the nef and the manifest are not a valid smart contract or the new contract is the
        same as the old one.
    """
    pass


def destroy_contract():
    """
    Destroy the executing smart contract
    """
    pass


NEO: UInt160 = UInt160(b'\x0a\x46\xe2\xe3\x7c\x99\x87\xf5\x70\xb4\xaf\x25\x3f\xb7\x7e\x7e\xef\x0f\x72\xb6')
GAS: UInt160 = UInt160(b'\xa6\xa6\xc1\x5d\xcd\xc9\xb9\x97\xda\xc4\x48\xb6\x92\x65\x22\xd2\x2e\xfe\xed\xfb')
