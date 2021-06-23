import ast
from typing import Dict, List

from boa3.model.builtin.interop.nativecontract import StdLibMethod
from boa3.model.variable import Variable


class StrSplitMethod(StdLibMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'split'
        syscall = 'stringSplit'
        args: Dict[str, Variable] = {
            'self': Variable(Type.str),
            'sep': Variable(Type.str),
            'maxsplit': Variable(Type.int)
        }
        # whitespace is the default separator
        separator_default = ast.parse("' '").body[0].value
        # maxsplit the default value is -1
        maxsplit_default = ast.parse("-1").body[0].value

        super().__init__(identifier, syscall, args, defaults=[separator_default, maxsplit_default],
                         return_type=Type.list.build_collection(Type.str))

    @property
    def generation_order(self) -> List[int]:
        """
        Gets the indexes order that need to be used during code generation.
        If the order for generation is the same as inputted in code, returns reversed(range(0,len_args))

        :return: Index order for code generation
        """
        indexes = super().generation_order
        maxsplit_index = list(self.args).index('maxsplit')

        indexes.remove(maxsplit_index)

        return indexes

    # TODO: Use maxsplit to verify if the returning array has length less than or equals to maxsplit and to concatenate if not
