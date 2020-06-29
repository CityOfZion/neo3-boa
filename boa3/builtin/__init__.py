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


class NeoMetadata:
    """
    This class stores the smart contract manifest information.

    :ivar has_storage: is a boolean value indicating whether the contract has a storage. False by default.
    :type has_storage: bool
    :ivar is_payable: is a boolean value indicating whether the contract accepts transfers. False by default.
    :type is_payable: bool
    """

    def __init__(self):
        self.has_storage: bool = False
        self.is_payable: bool = False
