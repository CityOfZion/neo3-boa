__all__ = [
    'ContractManagement',
    'Contract',
]


from typing import Any, Optional

from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160


class ContractManagement:
    """
    A class used to represent the ContractManagement native contract.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/native/ContractManagement>`__
    to learn more about the ContractManagement class.
    """

    hash: UInt160

    @classmethod
    def get_minimum_deployment_fee(cls) -> int:
        """
        Gets the minimum fee of contract deployment.

        >>> ContractManagement.get_minimum_deployment_fee()
        1000000000

        :return: the minimum fee of contract deployment
        """
        pass

    @classmethod
    def get_contract(cls, script_hash: UInt160) -> Optional[Contract]:
        """
        Gets a contract with a given hash. If the script hash is not associated with a smart contract, then it will
        return None.

        >>> ContractManagement.get_contract(UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2'))    # GAS script hash
        {
            'id': -6,
            'update_counter': 0,
            'hash': b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2',
            'nef': b'NEF3neo-core-v3.0\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00#\\x10A\\x1a\\xf7{g@\\x10A\\x1a\\xf7{g@\\x10A\\x1a\\xf7{g@\\x10A\\x1a\\xf7{g@\\x10A\\x1a\\xf7{g@QA\\xc7\\x9e',
            'manifest': {
                'name': 'GasToken',
                'group': [],
                'supported_standards': ['NEP-17'],
                'abi': [[['balanceOf', [['account', 20]], 17, 0, True], ['decimals', [], 17, 7, True], ['symbol', [], 19, 14, True], ['totalSupply', [], 17, 21, True], ['transfer', [['from', 20], ['to', 20], ['amount', 17], ['data', 0]], 16, 28, False]], [['Transfer', [['from', 20], ['to', 20], ['amount', 17]]]]],
                'permissions': [[None, None]],
                'trusts': [],
                'extras': 'null'
            },
        }

        >>> ContractManagement.get_contract(UInt160(bytes(20)))    # there is no smart contract associated with this script hash
        None

        :param script_hash: a smart contract hash
        :type script_hash: UInt160
        :return: a contract
        :rtype: Contract

        :raise Exception: raised if hash length isn't 20 bytes.
        """
        pass

    @classmethod
    def has_method(cls, hash: UInt160, method: str, parameter_count: int) -> bool:
        """
        Check if a method exists in a contract.

        >>> ContractManagement.has_method(UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2'),
        ...                               'balanceOf', 1)    # GAS script hash
        True

        >>> ContractManagement.has_method(UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2'),
        ...                               'balanceOf', 10)    # GAS script hash
        False

        >>> ContractManagement.has_method(UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2'),
        ...                               'invalid', 1)    # GAS script hash
        False

        :param hash: The hash of the deployed contract
        :type hash: UInt160
        :param method: The name of the method
        :type method: str
        :param parameter_count: The number of parameters
        :type parameter_count: int
        :return: whether the method exists or not
        :rtype: bool

        :raise Exception: raised if hash length isn't 20 bytes or if the parameter_count is less than 0.
        """
        pass

    @classmethod
    def deploy(cls, nef_file: bytes, manifest: bytes, data: Any = None) -> Contract:
        """
        Creates a smart contract given the script and the manifest.

        >>> nef_file_ = get_script(); manifest_ = get_manifest()    # get the script and manifest somehow
        ... ContractManagement.deploy(nef_file_, manifest_, None)             # smart contract will be deployed
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

    @classmethod
    def update(cls, nef_file: bytes, manifest: bytes, data: Any = None):
        """
        Updates the executing smart contract given the script and the manifest.

        >>> nef_file_ = get_script(); manifest_ = get_manifest()    # get the script and manifest somehow
        ... ContractManagement.update(nef_file_, manifest_, None)             # smart contract will be updated
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

    @classmethod
    def destroy(cls):
        """
        Destroy the executing smart contract.

        >>> ContractManagement.destroy()
        None

        """
        pass
