from abc import ABC, abstractmethod
from typing import List, Any

from boa3.model.type.itype import IType


class SequenceType(IType, ABC):
    """
    An interface used to represent Python sequence type
    """

    def __init__(self, identifier: str, values_type: List[IType]):
        self.value_type: IType = self.__initialize_sequence_type(values_type)
        super().__init__(identifier)

    @classmethod
    def get_types(cls, value: Any) -> List[IType]:
        from boa3.model.type.type import Type
        return list(set(map(Type.get_type, value)))  # get list of different types in the tuple

    @abstractmethod
    def is_valid_key(self, value_type: IType) -> bool:
        """
        Verifies if the given type is valid to retrieve values

        :param value_type: type to validate.
        :return: A boolean value that represents if the value is valid.
        """
        return False

    @property
    @abstractmethod
    def valid_key(self) -> IType:
        pass

    def __initialize_sequence_type(self, values_type: List[IType]):
        if len(values_type) != 1:
            from boa3.model.type.type import Type
            val_type = Type.none  # TODO: change to any when implemented
        else:
            val_type = values_type[0]

        return val_type

    @classmethod
    def filter_types(cls, values_type) -> List[IType]:
        if values_type is None:
            values_type = []
        elif not isinstance(values_type, list):
            values_type = [values_type]

        if len(values_type) > 1:
            # verifies if all the types are the same sequence with different arguments
            if all(isinstance(x, SequenceType) for x in values_type):
                sequence_type = type(values_type[0])
                if all(isinstance(x, sequence_type) for x in values_type):
                    types = list(set(value.value_type for value in values_type))
                    # if all the types are the same sequence type, build this sequence with any as parameters
                    values_type = [sequence_type(values_type=types)]
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
