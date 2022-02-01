from typing import Any, Dict, List, Tuple, Union

from boa3.constants import IMPORT_WILDCARD
from boa3.neo3.core.types import UInt160


def public(*args):
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
    :ivar extras: A json object with additional information. Empty by default;
    :vartype extras: Dict[str, Any]
    """

    def __init__(self):
        from typing import Optional

        self.supported_standards: List[str] = []
        self._trusts: List[str] = []

        # extras
        self.author: Optional[str] = None
        self.email: Optional[str] = None
        self.description: Optional[str] = None
        self.extras: Dict[str, Any] = {}

    @property
    def extra(self) -> Dict[str, Any]:
        """
        Gets the metadata extra information.

        :return: a dictionary that maps each extra value with its name. Empty by default
        """
        extra = self.extras.copy()
        if isinstance(self.author, str):
            extra['Author'] = self.author
        if isinstance(self.email, str):
            extra['Email'] = self.email
        if isinstance(self.description, str):
            extra['Description'] = self.description
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
            self._trusts.clear()
            self._trusts = [IMPORT_WILDCARD]

        # verifies if it's a valid contract hash
        elif hash_or_address.startswith('0x'):
            try:
                if len(UInt160.from_string(hash_or_address[2:])) == 20:
                    if hash_or_address not in self._trusts:
                        self._trusts.append(hash_or_address.lower())
            except ValueError:
                pass

        # verifies if it's a valid public key
        # compressed public keys in Neo start with either 03 or 02 and is followed by 32 bytes
        elif hash_or_address.startswith('03') or hash_or_address.startswith('02'):
            try:
                if len(bytes.fromhex(hash_or_address)) == 33:
                    if hash_or_address not in self._trusts:
                        self._trusts.append(hash_or_address.lower())
            except ValueError:
                pass
