from boa3.internal.model.builtin.method.printmethod import PrintMethod

from boa3.internal.model.type.itype import IType


class PrintByteStringMethod(PrintMethod):

    def __init__(self, arg_value: IType):
        from boa3.internal.model.type.primitive.bytestringtype import ByteStringType

        if not isinstance(arg_value, IType) or not ByteStringType.build().is_type_of(arg_value):
            from boa3.internal.model.type.type import Type
            arg_value = Type.str

        super().__init__(arg_value)
