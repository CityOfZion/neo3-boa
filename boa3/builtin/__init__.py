from typing import Any


def event(*args):
    """
    This decorator identifies a method that specifies a Neo event.
    The method's body is ignored when using this decorator and the function must have no return.
    """
    def event_wrapper():
        pass
    return event_wrapper


def public(*args):
    """
    This decorator identifies which methods should be included in the abi file
    """
    def public_wrapper():
        pass
    return public_wrapper


def metadata(*args):
    """
    This decorator identifies the function that returns the metadata object of the smart contract
    This can be used to only one function. Using this decorator in multiple functions will raise a compiler error.
    """
    def metadata_wrapper():
        pass
    return metadata_wrapper


def to_script_hash(data_bytes: Any) -> bytes:
    """
    Converts a data to a script hash.

    :param data_bytes: data to hash.
    :return: the script hash of the data
    :rtype: bytes
    """
    pass


class NeoMetadata:
    """
    This class stores the smart contract manifest information.

    :ivar has_storage: is a boolean value indicating whether the contract has a storage. False by default.
    :type has_storage: bool
    :ivar is_payable: is a boolean value indicating whether the contract accepts transfers. False by default.
    :type is_payable: bool
    :ivar author: the smart contract author. None by default;
    :type author: str or None
    :ivar email: the smart contract author email. None by default;
    :type email: str or None
    :ivar description: the smart contract description. None by default;
    :type description: str or None
    """

    from typing import Any, Dict

    def __init__(self):
        from typing import Optional

        # features
        self.has_storage: bool = False
        self.is_payable: bool = False

        # extras
        self.author: Optional[str] = None
        self.email: Optional[str] = None
        self.description: Optional[str] = None

    @property
    def extra(self) -> Dict[str, Any]:
        """
        Gets the metadata extra information

        :return: a dictionary that maps each extra value with its name. Empty by default.
        """
        extra = {}
        if isinstance(self.author, str):
            extra['Author'] = self.author
        if isinstance(self.email, str):
            extra['Email'] = self.email
        if isinstance(self.description, str):
            extra['Description'] = self.description
        return extra
