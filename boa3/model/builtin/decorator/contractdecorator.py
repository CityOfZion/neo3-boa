import ast
from typing import Dict, Sized

from boa3.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.model.variable import Variable


class ContractDecorator(IBuiltinDecorator):
    def __init__(self):
        from boa3.model.type.type import Type

        identifier = 'contract'
        args: Dict[str, Variable] = {'script_hash': Variable(Type.union.build([Type.str,
                                                                               Type.bytes]))}
        super().__init__(identifier, args)

    def build(self, *args) -> IBuiltinDecorator:
        if isinstance(args, Sized) and len(args) == 1 and isinstance(args[0], ast.AST):
            decorator = ContractDecorator()
            decorator._origin_node = args[0]
            return decorator

        return self

    @property
    def is_function_decorator(self) -> bool:
        return False

    @property
    def is_class_decorator(self) -> bool:
        return True
