from boa3.internal.model.builtin.classmethod.popmethod import PopMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class PopDictMethod(PopMethod):

    def __init__(self, arg_value: IType | None = None):
        from boa3.internal.model.type.type import Type

        if not Type.dict.is_type_of(arg_value):
            arg_value = Type.dict

        args: dict[str, Variable] = {
            'self': Variable(arg_value),
            'key': Variable(arg_value.valid_key)
        }

        super().__init__(args, return_type=arg_value.value_type)
