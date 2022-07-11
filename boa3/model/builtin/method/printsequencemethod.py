from boa3.model.builtin.method.printmethod import PrintMethod
from boa3.model.type.itype import IType


class PrintSequenceMethod(PrintMethod):

    def __init__(self, arg_value: IType):
        from boa3.model.type.type import Type

        if not isinstance(arg_value, IType) or not Type.sequence.is_type_of(arg_value):
            arg_value = Type.list

        super().__init__(arg_value)

    @property
    def is_supported(self) -> bool:
        # TODO: remove when print with sequences are implemented
        return False
