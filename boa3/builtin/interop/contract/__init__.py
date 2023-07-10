__all__ = [
    'CallFlags',
    'Contract',
    'ContractManifest',
    'call_contract',
    'create_contract',
    'update_contract',
    'destroy_contract',
    'get_minimum_deployment_fee',
    'get_call_flags',
    'create_standard_account',
    'create_multisig_account',
    'NEO',
    'GAS',
]


from typing import Any, List, Sequence

from boa3.builtin.interop.contract.callflagstype import CallFlags
from boa3.builtin.interop.contract.contract import Contract
from boa3.builtin.interop.contract.contractmanifest import ContractManifest
from boa3.builtin.type import ECPoint, UInt160


def call_contract(script_hash: UInt160, method: str, args: Sequence = (), call_flags: CallFlags = CallFlags.ALL) -> Any:
    """
    Calls a smart contract given the method and the arguments. Since the return is type Any, you'll probably need to
    type cast the return.

    >>> call_contract(NEO, 'balanceOf', [UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2')])
    100

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

    >>> nef_file_ = get_script(); manifest_ = get_manifest()    # get the script and manifest somehow
    ... create_contract(nef_file_, manifest_, None)             # smart contract will be deployed
    {
        'id': 2,
        'update_counter': 0,
        'hash': b'\\x92\\x8f+1q\\x86z_@\\x94\\xf5pE\\xcb\\xb8 \\x0f\\\\`Z',
        'nef': b'NEF3neo3-boa by COZ-1.0.0\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x07W\\x00\\x02xy\\x9e@\\xf9\\7b\\xbb\\xcc',
        'manifest': {
            'name': 'TestContract',
            'group': [],
            'supported_standards': [],
            'abi': [[['test', [['a', 17], ['b', 17]], 17, 0, False]], []],
            'permissions': [],
            'trusts': [],
            'extras': 'null'
        },
    }

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

    >>> nef_file_ = get_script(); manifest_ = get_manifest()    # get the script and manifest somehow
    ... update_contract(nef_file_, manifest_, None)             # smart contract will be updated
    None

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

    >>> destroy_contract()
    None

    """
    pass


def get_minimum_deployment_fee() -> int:
    """
    Gets the minimum fee of contract deployment.

    >>> get_minimum_deployment_fee()
    1000000000

    :return: the minimum fee of contract deployment
    """
    pass


def get_call_flags() -> CallFlags:
    """
    Gets the CallFlags in the current context.

    >>> get_call_flags()
    CallFlags.READ_ONLY
    """
    pass


def create_standard_account(pub_key: ECPoint) -> UInt160:
    """
    Calculates the script hash from a public key.

    >>> create_standard_account(ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'))
    b'\\r\\xa9g\\xa4\\x00C+\\xf2\\x7f\\x8e\\x8e\\xb4o\\xe8\\xace\\x9e\\xcc\\xde\\x04'

    :param pub_key: the given public key
    :type pub_key: ECPoint

    :return: the corresponding script hash of the public key
    :rtype: UInt160
    """
    pass


def create_multisig_account(m: int, pub_keys: List[ECPoint]) -> UInt160:
    """
    Calculates corresponding multisig account script hash for the given public keys.

    >>> create_multisig_account(1, [ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a')])
    b'"5,\\xd2\\x9e\\xe7\\xb4\\x02\\x08b\\xdbd\\x1e\\xedx\\x82\\x8fU(m'

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

>>> NEO
b'\\xf5c\\xea@\\xbc(=M\\x0e\\x05\\xc4\\x8e\\xa3\\x05\\xb3\\xf2\\xa0s@\\xef'

:meta hide-value:
"""

GAS: UInt160 = UInt160()
"""
GAS' token script hash.

>>> GAS
b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2'

:meta hide-value:
"""
