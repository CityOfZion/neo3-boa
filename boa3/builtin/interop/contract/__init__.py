from typing import Any, List, Sequence

from boa3.builtin.interop.contract.callflagstype import CallFlags
from boa3.builtin.interop.contract.contract import Contract
from boa3.builtin.type import ECPoint, UInt160


def call_contract(script_hash: UInt160, method: str, args: Sequence = (), call_flags: CallFlags = CallFlags.ALL) -> Any:
    """
    Calls a smart contract given the method and the arguments.

    :param script_hash: the target smart contract's script hash
    :type script_hash: UInt160
    :param method: the name of the method to be executed
    :type method: str
    :param args: the specified method's arguments
    :type args: Sequence[Any]
    :param call_flags: the CallFlags to be used to call the contract
    :type call_flags: CallFlags

    :return: the result of the specified method
    :rtype: Any

    :raise Exception: raised if there isn't a valid CallFlags, the script hash is not a valid smart contract or the
        method was not found or the arguments aren't valid to the specified method.
    """
    pass


def create_contract(nef_file: bytes, manifest: bytes, data: Any = None) -> Contract:
    """
    Creates a smart contract given the script and the manifest.

    :param nef_file: the target smart contract's compiled nef
    :type nef_file: bytes
    :param manifest: the manifest.json that describes how the script should behave
    :type manifest: bytes
    :param data: the parameters for the _deploy function
    :type data: Any

    :return: the contract that was created
    :rtype: Contract

    :raise Exception: raised if the nef or the manifest are not a valid smart contract.
    """
    pass


def update_contract(nef_file: bytes, manifest: bytes, data: Any = None):
    """
    Updates the executing smart contract given the script and the manifest.

    :param nef_file: the new smart contract's compiled nef
    :type nef_file: bytes
    :param manifest: the new smart contract's manifest
    :type manifest: bytes
    :param data: the parameters for the _deploy function
    :type data: Any

    :raise Exception: raised if the nef and the manifest are not a valid smart contract or the new contract is the
        same as the old one.
    """
    pass


def destroy_contract():
    """
    Destroy the executing smart contract.
    """
    pass


def get_minimum_deployment_fee() -> int:
    """
    Gets the minimum fee of contract deployment.

    :return: the minimum fee of contract deployment
    """
    pass


def get_call_flags() -> CallFlags:
    """
    Gets the CallFlags in the current context.
    """
    pass


def create_standard_account(pub_key: ECPoint) -> UInt160:
    """
    Calculates the script hash from a public key.

    :param pub_key: the given public key
    :type pub_key: ECPoint

    :return: the corresponding script hash of the public key
    :rtype: UInt160
    """
    pass


def create_multisig_account(m: int, pub_keys: List[ECPoint]) -> UInt160:
    """
    Calculates corresponding multisig account script hash for the given public keys.

    :param m: the minimum number of correct signatures need to be provided in order for the verification to pass.
    :type m: int
    :param pub_keys: the public keys of the account
    :type pub_keys: List[ECPoint]

    :return: the hash of the corresponding account
    :rtype: UInt160
    """
    pass


NEO: UInt160 = UInt160()
"""
NEO's token script hash.

:meta hide-value:
"""

GAS: UInt160 = UInt160()
"""
GAS' token script hash.

:meta hide-value:
"""
