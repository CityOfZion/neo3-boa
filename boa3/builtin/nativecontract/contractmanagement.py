from typing import Any

from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160


class ContractManagement:
    """
    A class used to represent the ContractManagement native contract
    """

    hash: UInt160

    @classmethod
    def get_minimum_deployment_fee(cls) -> int:
        """
        Gets the minimum fee of contract deployment.

        :return: the minimum fee of contract deployment
        """
        pass

    @classmethod
    def get_contract(cls, script_hash: UInt160) -> Contract:
        """
        Gets a contract with a given hash.

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
        """
        pass
