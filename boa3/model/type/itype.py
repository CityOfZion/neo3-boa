from abc import abstractmethod
from typing import Any

from boa3.model.symbol import ISymbol
from boa3.neo.vm.type.AbiType import AbiType


class IType(ISymbol):
    """
    An interface used to represent types

    :ivar identifier: the name identifier of the type
    """

    def __init__(self, identifier: str):
        self._identifier: str = identifier

    @property
    def shadowing_name(self) -> str:
        return 'type'

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def default_value(self) -> Any:
        return None

    @property
    def abi_type(self) -> AbiType:
        """
        Get the type representation for the abi

        :return: the representation for the abi. Any by default.
        """
        return AbiType.Any

    @classmethod
    @abstractmethod
    def _is_type_of(cls, value: Any) -> bool:
        """
        Validates if this is the type of the given value

        :param value: value to check the type
        :return: a boolean value that represents if this is the type of the value.
        :rtype: bool
        """
        pass

    def is_type_of(self, value: Any) -> bool:
        """
        Validates if this is the type of the given value. If this is not a primitive type, validates if its attributes
        are also valid.

        :param value: value to check the type
        :return: a boolean value that represents if this is the type of the value.
        :rtype: bool
        """
        return self._is_type_of(value)

    @classmethod
    @abstractmethod
    def build(cls, value: Any):
        """
        Creates a type instance with the given value

        :param value: value to build the type
        :return: The built type if the value is valid. None otherwise
        :rtype: IType or None
        """
        pass
