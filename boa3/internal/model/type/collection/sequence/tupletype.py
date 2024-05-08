from collections.abc import Iterable
from typing import Any

from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.itype import IType


class TupleType(SequenceType):
    """
    A class used to represent Python tuple type
    """

    def __init__(self, values_type: list[IType] = None, any_length: bool = False):
        identifier = 'tuple'
        if values_type is None:
            values_type = []
            any_length = True

        self._tuple_types = values_type
        self._is_any_length = any_length

        values_type = self.filter_types(values_type)
        super().__init__(identifier, values_type)

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self.item_type == Type.any and self._is_any_length:
            return self._identifier

        if len(self._tuple_types) == 0:
            tuple_types = [self.item_type.identifier]
        else:
            tuple_types = [type_.identifier for type_ in self._tuple_types]

        if self._is_any_length:
            tuple_types.append('...')
        return f'{self._identifier}[{", ".join(tuple_types)}]'

    @property
    def default_value(self) -> Any:
        return tuple()

    def is_valid_key(self, key_type: IType) -> bool:
        return key_type == self.valid_key

    @property
    def valid_key(self) -> IType:
        from boa3.internal.model.type.type import Type
        return Type.int

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            values_types: list[IType] = cls.get_types(value)
            from boa3.internal.model.type.type import Type
            if len(values_types) == 2 and values_types[-1] is Type.ellipsis:
                has_ellipsis = True
                values_types.pop()
            else:
                has_ellipsis = False
                if Type.ellipsis in values_types:
                    # only tuple[<type>, ...] is accepted as tuple of any size typed as <type>
                    # all other cases where ... is used it has the same behavior as any
                    for index, value in enumerate(values_types):
                        if value is Type.ellipsis:
                            values_types[index] = Type.any

            return cls(values_types, any_length=has_ellipsis)

    def build_any_length(self, value: Any) -> IType:
        result: TupleType = self.build((value,))
        if len(result._tuple_types) == 1:
            result._is_any_length = True
        return result

    @classmethod
    def build_collection(cls, *value_type: IType | Iterable) -> IType:
        params = []
        for arg in value_type:
            if isinstance(arg, Iterable):
                argument = list(arg)
            else:
                argument = [arg]
            params.extend(argument)
        return cls.build(tuple(params))

    @classmethod
    def get_types(cls, value: Any) -> list[IType]:
        from boa3.internal.model.type.type import Type
        return [val if isinstance(val, IType) else Type.get_type(val) for val in value]

    def get_item_type(self, index: tuple):
        if len(index) > 0 and isinstance(index[0], int):
            target_index = index[0]
            if len(self._tuple_types) > target_index:
                return self._tuple_types[target_index]

        return super().get_item_type(index)

    def is_type_of(self, value: Any) -> bool:
        if self._is_type_of(value):
            min_size = len(self._tuple_types)
            if isinstance(value, TupleType):
                types_to_check = value._tuple_types
                any_length = value._is_any_length
            else:
                types_to_check = value
                any_length = False

            len_types_to_check = len(types_to_check)
            if self._is_any_length and len_types_to_check == 0 and not any_length:
                # tuples of any length are always type of empty tuple
                return True
            if len_types_to_check < min_size:
                return False
            if not self._is_any_length:
                if len_types_to_check > min_size:
                    return False
                elif len_types_to_check == min_size and any_length:
                    return False

            for index in range(min_size):
                if not self._tuple_types[index].is_type_of(types_to_check[index]):
                    return False
            if len_types_to_check > min_size:
                last_tuple_type = self._tuple_types[-1] if len(self._tuple_types) else self.value_type
                for index in range(min_size, len_types_to_check):
                    if not last_tuple_type.is_type_of(types_to_check[index]):
                        return False

            return True
        return False

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) is tuple or isinstance(value, TupleType)

    @property
    def can_reassign_values(self) -> bool:
        return False

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.value_type == other.value_type

    def __hash__(self):
        return hash(self.identifier)
