import ast
from typing import Any, Dict, List, Sized

from boa3.internal.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.internal.model.variable import Variable
from boa3.internal.neo3.core.types import UInt160


class ContractDecorator(IBuiltinDecorator):
    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'contract'
        args: Dict[str, Variable] = {'script_hash': Variable(Type.union.build([Type.bytes,
                                                                               Type.str
                                                                               ]))}
        super().__init__(identifier, args)
        self.contract_hash = UInt160()

    def build(self, *args) -> IBuiltinDecorator:
        if isinstance(args, Sized) and len(args) > 0 and isinstance(args[0], ast.AST):
            decorator = ContractDecorator()
            decorator._origin_node = args[0]

            if len(args) > 1:
                values = self.validate_values(*args[:2])

                hash_arg = values[0] if len(values) > 0 else None
                if isinstance(hash_arg, UInt160):
                    decorator.contract_hash = hash_arg
            return decorator

        return self

    def validate_values(self, *params: Any) -> List[Any]:
        values = []
        if len(params) != 2:
            return values

        origin, visitor = params
        values.append(self.contract_hash)
        from boa3.internal.analyser.astanalyser import IAstAnalyser
        if not isinstance(visitor, IAstAnalyser):
            return values

        from boa3.internal.exception import CompilerError
        if not isinstance(origin, ast.Call) or len(origin.args) < 1:
            visitor._log_error(
                CompilerError.UnfilledArgument(origin.lineno, origin.col_offset, list(self.args.keys())[0])
            )
            return values
        argument_hash = visitor.visit(origin.args[0])

        try:
            if isinstance(argument_hash, str):
                from boa3.internal.neo import from_hex_str
                argument_hash = from_hex_str(argument_hash)

            if isinstance(argument_hash, bytes):
                values[0] = UInt160(argument_hash)
        except BaseException:
            visitor._log_error(CompilerError.InvalidUsage(origin.lineno,
                                                          origin.col_offset,
                                                          "Only literal values are accepted for 'script_hash' argument"
                                                          ))

        return values

    @property
    def is_function_decorator(self) -> bool:
        return False

    @property
    def is_class_decorator(self) -> bool:
        return True
