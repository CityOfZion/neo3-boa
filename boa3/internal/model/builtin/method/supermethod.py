from collections.abc import Sized
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.model.type.itype import IType


class SuperMethod(IBuiltinMethod):

    def __init__(self, value_type: IType = None):
        if isinstance(value_type, ClassType) and len(value_type.bases) > 0:
            # TODO: change when inheritance with multiple bases is implemented #2kq1gmc
            return_type = value_type.bases[0]
        else:
            from boa3.internal.model.type.type import Type
            return_type = Type.any

        identifier = 'super'
        self._super_type = value_type if isinstance(value_type, IType) else None
        super().__init__(identifier, return_type=return_type)

    @property
    def identifier(self) -> str:
        if self._super_type is None:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self._super_type._identifier)

    @property
    def is_supported(self) -> bool:
        return self._super_type is not None

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, Sized) and len(value) > 0:
            value = value[0]
        if value == self._super_type:
            return self
        if isinstance(value, IType):
            return SuperMethod(value)
        return super().build(value)
