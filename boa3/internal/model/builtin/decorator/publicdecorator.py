import ast
from typing import Any, Dict, List, Optional, Sized

from boa3.internal.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class PublicDecorator(IBuiltinDecorator):
    def __init__(self):
        identifier = 'public'
        args: Dict[str, Variable] = {'name': Variable(Type.str),
                                     'safe': Variable(Type.bool),
                                     }

        name_default = ast.parse("'{0}'".format(Type.str.default_value)).body[0].value
        safe_default = ast.parse("{0}".format(Type.bool.default_value)).body[0].value

        defaults = [name_default, safe_default]
        super().__init__(identifier, args, defaults)

        self.name: Optional[str] = None
        self.safe = False

    def build(self, *args) -> IBuiltinDecorator:
        if isinstance(args, Sized) and len(args) > 0 and isinstance(args[0], ast.AST):
            decorator = PublicDecorator()
            origin = args[0]
            decorator._origin_node = origin

            if len(args) > 1:
                values = self.validate_values(*args[:2])

                name_arg, safe_arg = values
                if isinstance(name_arg, str) and len(name_arg) > 0:
                    decorator.name = name_arg
                if isinstance(safe_arg, bool):
                    decorator.safe = safe_arg

            return decorator

        return self

    def validate_values(self, *params: Any) -> List[Any]:
        values = []
        if len(params) != 2:
            return values

        origin, visitor = params
        from boa3.internal.analyser.astanalyser import IAstAnalyser
        if not isinstance(origin, ast.Call) or not isinstance(visitor, IAstAnalyser):
            return [self.name, self.safe]

        # read the called arguments
        args_names = list(self.args.keys())
        args_len = min(len(origin.args), len(args_names))
        for x in range(args_len):
            values.append(visitor.visit(origin.args[x]))

        if len(values) <= 1:
            if len(values) == 0:
                values.append('')
            values.append(self.safe)

        # read the called keyword arguments
        for kwarg in origin.keywords:
            if kwarg.arg in args_names:
                x = args_names.index(kwarg.arg)
                value = visitor.visit(kwarg.value)
                values[x] = value

        from boa3.internal.exception import CompilerError
        name, safe = values
        if not isinstance(name, str):
            visitor._log_error(
                CompilerError.MismatchedTypes(
                    origin.lineno, origin.col_offset,
                    expected_type_id=Type.str.identifier,
                    actual_type_id=type(name).__name__
                ))

        if not isinstance(safe, bool):
            visitor._log_error(
                CompilerError.MismatchedTypes(
                    origin.lineno, origin.col_offset,
                    expected_type_id=Type.bool.identifier,
                    actual_type_id=type(safe).__name__
                ))

        return values
