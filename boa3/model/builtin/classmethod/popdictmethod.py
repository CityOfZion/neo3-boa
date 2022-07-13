from typing import Dict, Optional

from boa3.model.builtin.classmethod.popmethod import PopMethod
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class PopDictMethod(PopMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.model.type.type import Type

        if not Type.dict.is_type_of(arg_value):
            arg_value = Type.dict

        args: Dict[str, Variable] = {
            'self': Variable(arg_value),
            'key': Variable(arg_value.valid_key)
        }

        super().__init__(args, return_type=arg_value.value_type)
