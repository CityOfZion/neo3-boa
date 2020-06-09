from abc import ABC, abstractmethod
from typing import List, Any, Iterable

from boa3.model.type.itype import IType
from boa3.neo.vm.type.AbiType import AbiType


class SequenceType(IType, ABC):
    """
    An interface used to represent Python sequence type
    """

    def __init__(self, identifier: str, values_type: List[IType]):
        self.value_type: IType = self.__initialize_sequence_type(values_type)
        super().__init__(identifier)

    @property
    def identifier(self) -> str:
        return '{0}[{1}]'.format(self._identifier, self.value_type.identifier)

    @property
    def default_value(self) -> Any:
        return []

    def is_type_of(self, value: Any) -> bool:
        if self._is_type_of(value):
            if isinstance(value, SequenceType):
                return self.value_type.is_type_of(value.value_type)
            return True
        return False

    @classmethod
    def get_types(cls, value: Any) -> List[IType]:
        from boa3.model.type.type import Type
        if isinstance(value, IType):
            return [value]

        if not isinstance(value, Iterable):
            value = [value]

        types: List[IType] = [val if isinstance(val, IType) else Type.get_type(val) for val in value]
        types = list(set(types))  # get list of different types in the tuple
        return cls.filter_types(types)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Array  # TODO: change when 'bytes' is implemented

    @abstractmethod
    def is_valid_key(self, value_type: IType) -> bool:
        """
        Verifies if the given type is valid to retrieve values

        :param value_type: type to validate.
        :return: A boolean value that represents if the value is valid.
        """
        return False

    @property
    def can_reassign_values(self) -> bool:
        return True

    @property
    @abstractmethod
    def valid_key(self) -> IType:
        pass

    def __initialize_sequence_type(self, values_type: List[IType]):
        if len(values_type) != 1:
            from boa3.model.type.anytype import anyType
            val_type: IType = anyType
        else:
            val_type: IType = values_type[0]

        return val_type

    @classmethod
    def filter_types(cls, values_type) -> List[IType]:
        if values_type is None:
            values_type = []
        elif not isinstance(values_type, list):
            values_type = [values_type]

        if len(values_type) > 1:
            from boa3.model.type.type import Type
            if any(t is Type.any or t is Type.none for t in values_type):
                return [Type.any]

            # verifies if all the types are the same sequence with different arguments
            if all(isinstance(x, SequenceType) for x in values_type):
                sequence_type = type(values_type[0])  # first sequence type
                value_type = type(values_type[0].value_type)  # first sequence values type

                if all(isinstance(x, sequence_type) for x in values_type):
                    # if all the types are the same sequence type, build this sequence with any as parameters
                    types = list(set(value.value_type for value in values_type))
                    values_type = [sequence_type(values_type=types)]
                elif all(isinstance(x.value_type, value_type) for x in values_type):
                    # the sequences doesn't have the same type but the value type is the same
                    # for example: Tuple[int] and List[int]
                    values_type = [Type.sequence.build_sequence(values_type[0].value_type)]
                else:
                    # otherwise, built a generic sequence with any as parameters
                    values_type = [Type.sequence]
        return values_type

    @classmethod
    def build_sequence(cls, value_type: IType):
        """
        Creates a sequence type instance with the given value

        :param value_type: value to build the type
        :return: The built sequence type.
        :rtype: IType or None
        """
        return cls(values_type=[value_type])  # get list of different types in the tuple
