import ast
from collections.abc import Sized
from typing import Any

from boa3.internal.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.internal.model.variable import Variable


class DisplayNameDecorator(IBuiltinDecorator):
    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'display_name'
        args: dict[str, Variable] = {'name': Variable(Type.str)}
        super().__init__(identifier, args)
        self.external_name = None

    def build(self, *args) -> IBuiltinDecorator:
        if isinstance(args, Sized) and len(args) > 0 and isinstance(args[0], ast.AST):
            decorator = DisplayNameDecorator()
            decorator._origin_node = args[0]

            if len(args) > 1:
                values = self.validate_values(*args[:2])

                hash_arg = values[0] if len(values) > 0 else None
                if isinstance(hash_arg, str):
                    decorator.external_name = hash_arg
            return decorator

        return self

    def validate_values(self, *params: Any) -> list[Any]:
        values = []
        if len(params) != 2:
            return values

        origin, visitor = params
        values.append(self.external_name)
        from boa3.internal.analyser.astanalyser import IAstAnalyser
        if not isinstance(visitor, IAstAnalyser):
            return values

        from boa3.internal.exception import CompilerError
        if not isinstance(origin, ast.Call):
            visitor._log_error(
                CompilerError.UnfilledArgument(origin.lineno, origin.col_offset, list(self.args.keys())[0])
            )
            return values

        args_names = list(self.args.keys())
        if len(origin.args) > len(args_names):
            visitor._log_error(
                CompilerError.UnexpectedArgument(origin.lineno, origin.col_offset)
            )
            return values

        # read the called arguments
        args_len = min(len(origin.args), len(args_names))
        values.clear()

        for x in range(args_len):
            values.append(visitor.visit(origin.args[x]))

        if len(values) < 1:
            values.append(self.external_name)

        # read the called keyword arguments
        for kwarg in origin.keywords:
            if kwarg.arg in args_names:
                x = args_names.index(kwarg.arg)
                value = visitor.visit(kwarg.value)
                values[x] = value
            else:
                visitor._log_error(
                    CompilerError.UnexpectedArgument(kwarg.lineno, kwarg.col_offset)
                )

        if not isinstance(values[0], str):
            visitor._log_error(
                CompilerError.UnfilledArgument(origin.lineno, origin.col_offset, list(self.args.keys())[0])
            )
            return values

        if visitor.get_symbol(values[0]) is not None:
            visitor._log_error(CompilerError.InvalidUsage(origin.lineno,
                                                          origin.col_offset,
                                                          "Only literal values are accepted for 'name' argument"
                                                          ))
            values[0] = self.external_name

        return values

    @property
    def is_function_decorator(self) -> bool:
        return True

    @property
    def is_class_decorator(self) -> bool:
        return False
