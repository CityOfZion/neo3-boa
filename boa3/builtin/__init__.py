from typing import Any, Dict, List, Tuple, Union

from boa3.constants import IMPORT_WILDCARD
from boa3.neo3.core.types import UInt160


def public(*args, **kwargs):
    """
    This decorator identifies which methods should be included in the abi file.
    """

    def public_wrapper():
        pass

    return public_wrapper


def metadata(*args):
    """
    This decorator identifies the function that returns the metadata object of the smart contract.
    This can be used to only one function. Using this decorator in multiple functions will raise a compiler error.
    """

    def metadata_wrapper():
        pass

    return metadata_wrapper


def contract(script_hash: Union[str, bytes]):
    """
    This decorator identifies a class that should be interpreted as an interface to an existing contract.
    """
    pass


def to_script_hash(data_bytes: Any) -> bytes:
    """
    Converts a data to a script hash.

    :param data_bytes: data to hash
    :type data_bytes: Any
    :return: the script hash of the data
    :rtype: bytes
    """
    pass


def Event(*args, **kwargs):
    """
    Describes an action that happened in the blockchain.
    """
    pass


def CreateNewEvent(arguments: List[Tuple[str, type]] = [], event_name: str = '') -> Event:
    """
    Creates a new event.

    :param arguments: the list of the events args' names and types
    :type arguments: List[Tuple[str, type]]
    :param event_name: custom name of the event. It's filled with the variable name if not specified
    :type event_name: str
    :return: the new event
    :rtype: Event
    """
    pass


class NeoMetadata:
    """
    This class stores the smart contract manifest information.

    :ivar supported_standards: Neo standards supported by this smart contract. Empty by default;
    :vartype supported_standards: List[str]
    :ivar trusts: a list of contracts that this smart contract trust. Empty by default;
    :vartype trusts: List[str]
    :ivar author: the smart contract author. None by default;
    :vartype author: str or None
    :ivar email: the smart contract author email. None by default;
    :vartype email: str or None
    :ivar description: the smart contract description. None by default;
    :vartype description: str or None
    """

    def __init__(self):
        self.supported_standards: List[str] = []
        self._trusts: List[str] = []
        self._permissions: List[dict] = []

    @property
    def extras(self) -> Dict[str, Any]:
        """
        Gets the metadata extra information.

        :return: a dictionary that maps each extra value with its name. Empty by default
        """
        # list the variables names that are part of the manifest
        specific_field_names = ['supported_standards',
                                ]
        extra = {}

        for var_name, var_value in vars(self).items():
            if var_name in specific_field_names:
                continue

            if var_value is not None and not var_name.startswith('_'):
                extra_field = var_name.title().replace('_', '')
                extra[extra_field] = var_value

        return extra

    def add_trusted_source(self, hash_or_address: str):
        """
        Adds a valid contract hash, valid group public key, or the * wildcard to trusts.

        :param hash_or_address: a contract hash, group public key or *
        :type hash_or_address: str
        """
        if not isinstance(hash_or_address, str):
            return

        if self._trusts == [IMPORT_WILDCARD]:
            return

        if hash_or_address == IMPORT_WILDCARD:
            self._trusts = [IMPORT_WILDCARD]

        # verifies if it's a valid contract hash
        elif self.verify_is_valid_contract_hash(hash_or_address):
            if hash_or_address not in self._trusts:
                self._trusts.append(hash_or_address.lower())

        # verifies if it's a valid public key
        elif self.verify_is_valid_public_key(hash_or_address):
            if hash_or_address not in self._trusts:
                self._trusts.append(hash_or_address.lower())

    def add_permission(self, *, contract: str = None, methods: Union[List[str], str] = None):
        """
        Adds a valid contract and a valid methods to the permissions in the manifest.

        :param contract: a contract hash, group public key or *
        :type contract: str
        :param methods: a list of methods or *
        :type methods: Union[List[str], str]
        """

        if contract is None and methods is None:
            return

        if not isinstance(contract, str) and contract is not None:
            return

        if not isinstance(methods, (str, list)) and methods is not None:
            return

        all_permissions = {
            'contract': IMPORT_WILDCARD,
            'methods': IMPORT_WILDCARD,
        }

        if all_permissions in self._permissions:
            return

        # verifies if contract is a valid value
        elif contract is not None and (not self.verify_is_valid_contract_hash(contract) and
                                       not self.verify_is_valid_public_key(contract) and
                                       contract != IMPORT_WILDCARD):
            return

        # verifies if methods is a valid value
        elif ((isinstance(methods, str) and methods != '*') or
              (isinstance(methods, list) and any(not isinstance(method, str) for method in methods))):
            return

        new_permission = {
            'contract': contract.lower() if contract is not None else IMPORT_WILDCARD,
            'methods': methods if methods is not None else IMPORT_WILDCARD,
        }

        if new_permission == all_permissions:
            self._permissions = [new_permission]

        elif new_permission not in self._permissions:
            self._permissions.append(new_permission)

    @staticmethod
    def verify_is_valid_public_key(public_key: str) -> bool:
        # compressed public keys in Neo start with either 03 or 02 and is followed by 32 bytes
        if public_key.startswith('03') or public_key.startswith('02'):
            try:
                if len(bytes.fromhex(public_key)) == 33:
                    return True
            except ValueError:
                pass
        return False

    @staticmethod
    def verify_is_valid_contract_hash(contract_hash: str) -> bool:
        if contract_hash.startswith('0x'):
            try:
                if len(UInt160.from_string(contract_hash[2:])) == 20:
                    return True
            except ValueError:
                pass
        return False
