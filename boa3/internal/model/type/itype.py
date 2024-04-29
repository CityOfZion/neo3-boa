from abc import abstractmethod
from typing import Any, Self

from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.symbol import ISymbol
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.StackItem import StackItemType


class IType(IdentifiedSymbol):
    """
    An interface used to represent types

    :ivar identifier: the name identifier of the type
    """

    def __init__(self, identifier: str, deprecated: bool = False):
        super().__init__(identifier, deprecated)

    @property
    def shadowing_name(self) -> str:
        return 'type'

    def __repr__(self) -> str:
        return self.__str__()

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
    def build(cls, value: Any) -> Self:
        """
        Creates a type instance with the given value

        :param value: value to build the type
        :return: The built type if the value is valid. None otherwise
        :rtype: IType or None
        """
        pass

    def generate_is_instance_type_check(self, code_generator):
        """
        Generates the opcodes to check if a value is of this type

        :type code_generator: boa3.internal.compiler.codegenerator.codegenerator.CodeGenerator
        """
        code_generator.insert_type_check(self.stack_item)

    @property
    def symbols(self) -> dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the class type with its name
        """
        return {}

    def union_type(self, other_type: "IType") -> "IType":
        """
        Gets a type that is an union of `self` and `other_type`

        :param other_type: type that'll be united with `self`
        :type other_type: IType
        :return: an union of this type and other_type
        :rtype: IType
        """
        from boa3.internal.model.type.annotation.uniontype import UnionType
        return UnionType.build((self, other_type))

    def except_type(self, other_type: "IType") -> "IType":
        """
        Gets a type that is type of `self` but is not type of `other_type`.
        If `other_type` is an implementation of `self`, returns `self`

        :param other_type: type that won't be allowed in the resulting type
        :type other_type: IType
        :return: an union of this type and the exclusion of other_type
        :rtype: IType
        """
        return self

    def intersect_type(self, other_type: "IType") -> "IType":
        """
        Gets a type that is the intersection of `self` but is not type of `other_type`.
        If `other_type` is an implementation of `self`, returns `other_type`
        If `other_type` and `self` has no values in common, returns None

        :param other_type: type that'll be intersected with self
        :type other_type: IType
        :return: an intersection of this type and the exclusion of other_type
        :rtype: IType
        """
        if self.is_type_of(other_type):
            return other_type
        if other_type.is_type_of(self):
            return self

        from boa3.internal.model.type.annotation.uniontype import UnionType
        if isinstance(other_type, UnionType):
            same_types = [x for x in other_type.union_types if self.is_type_of(x)]
            if len(same_types) == 0:
                return self
            elif len(same_types) == 1:
                return same_types[0]
            else:
                return UnionType.build(same_types)

        from boa3.internal.model.type.type import Type
        return Type.none

    def is_equal(self, other: Any) -> bool:
        if not isinstance(other, IType):
            return False
        return self.is_type_of(other) and other.is_type_of(self)
