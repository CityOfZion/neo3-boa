__all__ = [
    'CreateNewEvent',
    'public',
    'metadata',
    'contract',
    'display_name',
    'NeoMetadata',
]

from typing import List, Dict, Any, Union, Optional, Tuple

from boa3.builtin.type import Event


def CreateNewEvent(arguments: List[Tuple[str, type]] = [], event_name: str = '') -> Event:
    """
    Creates a new Event.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/develop/write/basics#events>`__ to learn more
    about Events.

    >>> new_event: Event = CreateNewEvent(
    ...     [
    ...        ('name', str),
    ...        ('amount', int)
    ...     ],
    ...     'New Event'
    ... )

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
    This decorator identifies which methods should be included in the abi file. Adding this decorator to a function
    means it could be called externally.

    >>> @public     # this method will be added to the abi
    ... def callable_function() -> bool:
    ...     return True
    {
        "name": "callable_function",
        "offset": 0,
        "parameters": [],
        "safe": false,
        "returntype": "Boolean"
    }

    >>> @public(name='callableFunction')     # the method will be added with the different name to the abi
    ... def callable_function() -> bool:
    ...     return True
    {
        "name": "callableFunction",
        "offset": 0,
        "parameters": [],
        "safe": false,
        "returntype": "Boolean"
    }

    >>> @public(safe=True)      # the method will be added with the safe flag to the abi
    ... def callable_function() -> bool:
    ...     return True
    {
        "name": "callable_function",
        "offset": 0,
        "parameters": [],
        "safe": true,
        "returntype": "Boolean"
    }

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

    Deprecated in 1.1.1. Will be removed in 1.2.0

    >>> @metadata   # this indicates that this function will have information about the smart contract
    ... def neo_metadata() -> NeoMetadata:      # needs to return a NeoMetadata
    ...     meta = NeoMetadata()
    ...     meta.name = 'NewContractName'
    ...     return meta
    """
    pass


def contract(script_hash: Union[str, bytes]):
    """
    This decorator identifies a class that should be interpreted as an interface to an existing contract.

    If you want to use the script hash in your code, you can use the `hash` class attribute that automatically maps the
    script hash parameter onto it. You don't need to declare it in your class, but your IDE might send a warning about
    the attribute if you don't.

    Check out `Our Documentation <https://dojo.coz.io/neo3/boa/calling-smart-contracts.html#with-interface>`__ to learn
    more about this decorator.

    >>> @contract('0xd2a4cff31913016155e38e474a2c06d08be276cf')
    ... class GASInterface:
    ...     hash: UInt160      # you don't need to declare this class variable, we are only doing it to avoid IDE warnings
    ...                        # but if you do declare, you need to import the type UInt160 from boa3.builtin.type
    ...     @staticmethod
    ...     def symbol() -> str:
    ...         pass
    ... @public
    ... def main() -> str:
    ...     return "Symbol is " + GASInterface.symbol()
    ... @public
    ... def return_hash() -> UInt160:
    ...     return GASInterface.hash    # neo3-boa will understand that this attribute exists even if you don't declare it

    :param script_hash: Script hash of the interfaced contract
    :type script_hash: str or bytes
    """
    def decorator_wrapper(cls, *args, **kwargs):
        if isinstance(script_hash, str):
            from boa3.internal.neo import from_hex_str
            _hash = from_hex_str(script_hash)
        else:
            _hash = script_hash

        cls.hash = _hash
        return cls
    return decorator_wrapper


def display_name(name: str):
    """
    This decorator identifies which methods from a contract interface should have a different identifier from the one
    interfacing it. It only works in contract interface classes.

    >>> @contract('0xd2a4cff31913016155e38e474a2c06d08be276cf')
    ... class GASInterface:
    ...     @staticmethod
    ...     @display_name('totalSupply')
    ...     def total_supply() -> int:      # the smart contract will call "totalSupply", but when writing the script you can call this method whatever you want to
    ...         pass
    ... @public
    ... def main() -> int:
    ...     return GASInterface.total_supply()

    :param name: Method identifier from the contract manifest.
    :type name: str
    """
    def decorator_wrapper(*args, **kwargs):
        pass
    return decorator_wrapper


class NeoMetadata:
    """
    This class stores the smart contract manifest information.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/develop/write/manifest>`__ to learn more about
    the Manifest.

    >>> def neo_metadata() -> NeoMetadata:
    ...     meta = NeoMetadata()
    ...     meta.name = 'NewContractName'
    ...     meta.add_permission(methods=['onNEP17Payment'])
    ...     meta.add_trusted_source("0x1234567890123456789012345678901234567890")
    ...     meta.date = "2023/05/30"    # this property will end up inside the extra property
    ...     return meta

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

        >>> self.add_trusted_source("0x1234567890123456789012345678901234abcdef")

        >>> self.add_trusted_source("035a928f201639204e06b4368b1a93365462a8ebbff0b8818151b74faab3a2b61a")

        >>> self.add_trusted_source("*")

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

        >>> self.add_group("031f64da8a38e6c1e5423a72ddd6d4fc4a777abe537e5cb5aa0425685cda8e063b",
        ...                "fhsOJNF3N5Pm3oV1b7wYTx0QVelYNu7whwXMi8GsNGFKUnu3ZG8z7oWLfzzEz9pbnzwQe8WFCALEiZhLD1jG/w==")

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

        >>> self.add_permission(methods=['onNEP17Payment'])

        >>> self.add_permission(contract='0x3846a4aa420d9831044396dd3a56011514cd10e3', methods=['get_object'])

        >>> self.add_permission(contract='0333b24ee50a488caa5deec7e021ff515f57b7993b93b45d7df901e23ee3004916')

        :param contract: a contract hash, group public key or '*'
        :type contract: str
        :param methods: a list of methods or '*'
        :type methods: Union[List[str], str]
        """

        if isinstance(contract, bytes):
            try:
                from boa3.internal.neo3.core.types import UInt160
                contract = str(UInt160(contract))
            except BaseException:
                pass

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

        from boa3.internal import constants
        wildcard_permission = {
            'contract': constants.IMPORT_WILDCARD,
            'methods': constants.IMPORT_WILDCARD,
        }

        if wildcard_permission not in self._permissions:
            new_permission = {
                'contract': contract.lower(),
                'methods': methods,
            }

            if contract == constants.IMPORT_WILDCARD and methods == constants.IMPORT_WILDCARD:
                self._permissions.clear()
                self._permissions.append(wildcard_permission)
            elif new_permission not in self._permissions:
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
