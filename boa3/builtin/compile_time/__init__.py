from typing import List, Dict, Any, Union, Optional, Tuple

from boa3.builtin.type import ByteString, Event


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


def public(name: str = None, safe: bool = True, *args, **kwargs):
    """
    This decorator identifies which methods should be included in the abi file.

    :param name: Identifier for this method that'll be used on the abi. If not specified, it'll be the same
     identifier from Python method definition
    :type name: str
    :param safe: Whether this method is an abi safe method. False by default
    :type safe: bool
    """
    def decorator_wrapper(*args, **kwargs):
        pass
    return decorator_wrapper


def metadata(*args):
    """
    This decorator identifies the function that returns the metadata object of the smart contract.
    This can be used to only one function. Using this decorator in multiple functions will raise a compiler error.
    """
    pass


def contract(script_hash: ByteString):
    """
    This decorator identifies a class that should be interpreted as an interface to an existing contract.

    :param script_hash: Script hash of the interfaced contract
    :type script_hash: str or bytes
    """
    def decorator_wrapper(cls, *args, **kwargs):
        cls.hash = script_hash
        return cls
    return decorator_wrapper


def display_name(name: str):
    """
    This decorator identifies which methods from a contract interface should have a different identifier from the one
    interfacing it. It only works in contract interface classes.

    :param name: Method identifier from the contract manifest.
    :type name: str
    """
    pass


class NeoMetadata:
    """
    This class stores the smart contract manifest information.

    :ivar name: the smart contract name. Will be the name of the file by default;
    :vartype type name: str
    :ivar supported_standards: Neo standards supported by this smart contract. Empty by default;
    :vartype supported_standards: List[str]
    :ivar permissions: a list of contracts and methods that this smart contract permits to invoke and call. All
     contracts and methods permitted by default;
    :vartype permissions: List[str]
    :ivar trusts: a list of contracts that this smart contract trust. Empty by default;
    :vartype trusts: List[str]
    :ivar author: the smart contract author. None by default;
    :vartype author: str or None
    :ivar email: the smart contract author email. None by default;
    :vartype email: str or None
    :ivar description: the smart contract description. None by default;
    :vartype description: str or None
    """
    from boa3.internal.constants import IMPORT_WILDCARD

    def __init__(self):
        self.name: str = ''
        self.source: Optional[str] = None
        self.supported_standards: List[str] = []
        self._trusts: List[str] = []
        self._permissions: List[dict] = []
        self._groups: List[dict] = []

    @property
    def extras(self) -> Dict[str, Any]:
        """
        Gets the metadata extra information.

        :return: a dictionary that maps each extra value with its name. Empty by default
        """
        # list the variables names that are part of the manifest
        specific_field_names = ['name',
                                'source',
                                'supported_standards',
                                ]
        extra = {}

        for var_name, var_value in vars(self).items():
            if var_name in specific_field_names:
                continue

            if var_value is not None and not var_name.startswith('_'):
                extra_field = var_name.title().replace('_', '')
                extra[extra_field] = var_value

        return extra

    @property
    def trusts(self) -> List[str]:
        from boa3.internal.constants import IMPORT_WILDCARD
        if self._trusts == [IMPORT_WILDCARD]:
            return IMPORT_WILDCARD
        return self._trusts.copy()

    @property
    def permissions(self) -> List[dict]:
        return self._permissions.copy()

    @property
    def groups(self) -> List[dict]:
        return self._groups.copy()

    def add_trusted_source(self, hash_or_address: str):
        """
        Adds a valid contract hash, valid group public key, or the '*' wildcard to trusts.

        :param hash_or_address: a contract hash, group public key or '*'
        :type hash_or_address: str
        """
        if not isinstance(hash_or_address, str):
            return

        from boa3.internal.constants import IMPORT_WILDCARD
        if self._trusts == [IMPORT_WILDCARD]:
            return

        if hash_or_address == IMPORT_WILDCARD:
            self._trusts = [IMPORT_WILDCARD]

        # verifies if it's a valid contract hash
        elif self._verify_is_valid_contract_hash(hash_or_address):
            if hash_or_address not in self._trusts:
                self._trusts.append(hash_or_address.lower())

        # verifies if it's a valid public key
        elif self._verify_is_valid_public_key(hash_or_address):
            if hash_or_address not in self._trusts:
                self._trusts.append(hash_or_address.lower())

    def add_group(self, pub_key: str, signature: str):
        """
        Adds a pair of public key and signature to the groups in the manifest.

        :param pub_key: public key of the group
        :type pub_key: str
        :param signature: signature of the contract hash encoded in Base64
        :type signature: str
        """

        if not isinstance(pub_key, str) or not isinstance(signature, str):
            return

        # verifies if pub_key is a valid value
        if not self._verify_is_valid_public_key(pub_key):
            return

        new_group = {
            'pubkey': pub_key.lower(),
            'signature': signature,
        }

        if new_group not in self._permissions:
            self._groups.append(new_group)

    def add_permission(self, *, contract: str = IMPORT_WILDCARD, methods: Union[List[str], str] = IMPORT_WILDCARD):
        """
        Adds a valid contract and a valid methods to the permissions in the manifest.

        :param contract: a contract hash, group public key or '*'
        :type contract: str
        :param methods: a list of methods or '*'
        :type methods: Union[List[str], str]
        """

        if not isinstance(contract, str):
            return

        if not isinstance(methods, (str, list)):
            return

        from boa3.internal.constants import IMPORT_WILDCARD
        # verifies if contract is a valid value
        if (not self._verify_is_valid_contract_hash(contract) and
                not self._verify_is_valid_public_key(contract) and
                contract != IMPORT_WILDCARD):
            return

        # verifies if methods is a valid value
        elif ((isinstance(methods, str) and methods != IMPORT_WILDCARD) or
              (isinstance(methods, list) and any(not isinstance(method, str) for method in methods))):
            return

        # if both values are the import wildcard, then it's not necessary to include it in the manifest
        if contract == '*' and methods == '*':
            return

        new_permission = {
            'contract': contract.lower(),
            'methods': methods,
        }

        if new_permission not in self._permissions:
            self._permissions.append(new_permission)

    @staticmethod
    def _verify_is_valid_public_key(public_key: str) -> bool:
        """
        Verifies if a given compressed public key is valid.

        :return: whether the given public key is valid or not
        """
        if public_key.startswith('03') or public_key.startswith('02'):
            try:
                from boa3.internal import constants
                if len(bytes.fromhex(public_key)) == constants.SIZE_OF_ECPOINT:
                    return True
            except ValueError:
                pass
        return False

    @staticmethod
    def _verify_is_valid_contract_hash(contract_hash: str) -> bool:
        """
        Verifies if a given contract hash is valid.

        :return: whether the given contract hash is valid or not
        """
        if contract_hash.startswith('0x'):
            try:
                from boa3.internal.neo3.core.types import UInt160
                # if contract_hash is not a valid UInt160, it will raise a ValueError
                UInt160.from_string(contract_hash[2:])
                return True
            except ValueError:
                pass
        return False
