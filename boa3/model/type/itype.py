from abc import abstractmethod
from typing import Any, Dict

from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.symbol import ISymbol
from boa3.neo.vm.type.AbiType import AbiType
from boa3.neo.vm.type.StackItemType import StackItemType


class IType(IdentifiedSymbol):
    """
    An interface used to represent types

    :ivar identifier: the name identifier of the type
    """

    def __init__(self, identifier: str):
        super().__init__(identifier)

    @property
    def shadowing_name(self) -> str:
        return 'type'

    def __str__(self) -> str:
        return self.identifier

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

    @property
    def stack_item(self) -> StackItemType:
        """
        Get the Neo VM stack item type representation for this type

        :return: the stack item type of this type. Any by default.
        """
        return StackItemType.Any

    @property
    def is_generic(self) -> bool:
        """
        Verifies if this is a generic type

        :return: True if this is a generic type. False otherwise.
        """
        return False

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

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the class type with its name
        """
        return {}
