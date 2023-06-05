from boa3.internal.model.builtin.method.printmethod import PrintMethod

from boa3.internal.model.type.itype import IType


class PrintByteStringMethod(PrintMethod):

    def __init__(self, arg_value: IType):
        from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType

        if not isinstance(arg_value, IType) or not isinstance(arg_value, IByteStringType):
            from boa3.internal.model.type.type import Type
            arg_value = Type.str

        super().__init__(arg_value)
