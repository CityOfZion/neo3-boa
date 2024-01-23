from collections.abc import Sized
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.annotation.metatype import MetaType, metaType
from boa3.internal.model.type.anytype import anyType
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class CastTypeMethod(IBuiltinMethod):

    def __init__(self, cast_to_type: IType = None, origin_type: IType = None):
        # if the type to be casted is not value, there's an error in the signature
        if cast_to_type is None:
            type_value = metaType
        elif isinstance(cast_to_type, MetaType):
            type_value = cast_to_type if cast_to_type.has_meta_type else metaType
        else:
            type_value = MetaType.build(cast_to_type)

        if origin_type is None:
            origin_type = anyType
        elif isinstance(origin_type, MetaType):
            origin_type = origin_type.meta_type if origin_type.has_meta_type else anyType

        identifier = 'cast'
        args: dict[str, Variable] = {'typ': Variable(type_value),
                                     'val': Variable(anyType)}
        super().__init__(identifier, args,
                         return_type=cast_to_type.meta_type if isinstance(cast_to_type, MetaType) else anyType)
        self._origin_type: IType = origin_type

    @property
    def identifier(self) -> str:
        if self.is_supported:
            identifier = (self.typ_arg.type.meta_id
                          if hasattr(self.typ_arg.type, 'meta_id')
                          else self.typ_arg.type.identifier)
            return '-{0}_{1}'.format(self._identifier, identifier)
        else:
            return self._identifier

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        if not isinstance(params[0], IExpression):
            return False
        return isinstance(params[0].type, SequenceType)

    @property
    def is_supported(self) -> bool:
        return (isinstance(self.typ_arg, Variable)
                and isinstance(self.typ_arg.type, MetaType)
                and self.typ_arg.type.has_meta_type)

    def not_supported_str(self, callable_id: str) -> str:
        return '{0}({1})'.format(callable_id,
                                 ','.join([arg.type.identifier if isinstance(arg, Variable) else 'unknown'
                                           for arg in self.args.values()]))

    @property
    def is_cast(self) -> bool:
        return True

    @property
    def cast_types(self) -> tuple[IType, IType] | None:
        origin_type = self._origin_type
        target_type = (self.typ_arg.type.meta_type
                       if hasattr(self.typ_arg.type, 'meta_type')
                       else self.typ_arg.type)
        return origin_type, target_type

    def generate_internal_opcodes(self, code_generator):
        pass

    @property
    def _args_on_stack(self) -> int:
        return 1  # the implementation is the same as x = arg

    @property
    def args_on_stack(self) -> int:
        return 1  # the implementation is the same as x = arg

    @property
    def generation_order(self) -> list[int]:
        # type should not be converted
        indexes = super().generation_order
        typ_index = list(self.args).index('typ')

        if typ_index in indexes:
            indexes.remove(typ_index)

        return indexes

    @property
    def _body(self) -> str | None:
        return None

    @property
    def typ_arg(self) -> Variable:
        return self.args['typ'] if isinstance(self.args['typ'], Variable) else Variable(anyType)

    @property
    def val_arg(self) -> Variable:
        return self.args['val']

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, Sized) and len(value) == len(self.args):
            cast_to = value[0]
            cast_from = value[1]

            if isinstance(cast_to, IType):
                if isinstance(cast_from, IType):
                    return CastTypeMethod(cast_to, cast_from)
                else:
                    return CastTypeMethod(cast_to)
        return super().build(value)
