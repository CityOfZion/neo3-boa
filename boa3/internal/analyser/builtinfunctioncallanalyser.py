import ast
from collections.abc import Callable
from typing import Any

from boa3.internal.analyser.astanalyser import IAstAnalyser
from boa3.internal.exception import CompilerError
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.builtin.method.isinstancemethod import IsInstanceMethod
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType


class BuiltinFunctionCallAnalyser(IAstAnalyser):
    def __init__(self, origin: IAstAnalyser, call: ast.Call, method_id: str, builtin_method: IBuiltinMethod,
                 log: bool, fail_fast: bool = True):
        self._method: IBuiltinMethod = builtin_method
        self.method_id: str = method_id
        super().__init__(call, root_folder=origin.root_folder, log=log, fail_fast=fail_fast)

        self._origin: IAstAnalyser = origin

        # all methods validators must be (IBuiltinMethod, list[IType]) -> None
        self._methods_validators: dict[type[IBuiltinMethod],
                                       Callable[[IBuiltinMethod, list[IType]], None]] = {
            IsInstanceMethod: self._validate_IsInstanceMethod
        }

    @property
    def method(self) -> IBuiltinMethod:
        return self._method

    @property
    def call(self) -> ast.Call:
        return self._tree

    def get_symbol(self, symbol_id: str,
                   is_internal: bool = False,
                   check_raw_id: bool = False) -> ISymbol | None:
        return self._origin.get_symbol(symbol_id, is_internal)

    def get_symbol_from_node(self, node: ast.AST) -> ISymbol | None:
        if isinstance(node, ast.Name):
            return self.get_symbol(node.id)

        if isinstance(node, ast.Attribute):
            value = self.get_symbol_from_node(node.value)
            if hasattr(value, 'symbols') and node.attr in value.symbols:
                return value.symbols[node.attr]

        return None

    def get_type(self, value: Any, use_metadata: bool = False) -> IType:
        return self._origin.get_type(value, use_metadata)

    def validate(self) -> bool:
        """
        Validates the method arguments.

        :return: whether the method have specific validation
        """
        if type(self.method) in self._methods_validators:
            if self.method_id == self.method.raw_identifier:
                # if the identifiers are diffrente, this method was validated already
                validator = self._methods_validators[type(self.method)]
                args = [self.get_type(param) for param in self.call.args]
                validator(self.method, args)
            return True
        return False

    def _validate_IsInstanceMethod(self, method: IsInstanceMethod, args_types: list[IType]):
        """
        Validates the arguments for `isinstance` method

        :param method: instance of the builtin method
        :param args_types: types of the arguments
        """
        last_arg = self.call.args[-1]
        if isinstance(last_arg, ast.Tuple) and all(isinstance(tpe, (ast.Attribute, ast.Name))
                                                   for tpe in last_arg.elts):
            if len(last_arg.elts) == 1:
                # if the types tuple has only one type, remove it from inside the tuple
                last_arg = self.call.args[-1] = last_arg.elts[-1]
                args_types[-1] = args_types[-1].value_type
            elif len(last_arg.elts) > 1:
                # if there are more than one type, updates information in the instance of the method
                types: list[IType] = [self.get_symbol_from_node(name) for name in last_arg.elts]
                method.set_instance_type(types)
                self.call.args[-1] = last_arg.elts[-1]
                return

        from boa3.internal.model.type.annotation.metatype import MetaType
        from boa3.internal.model.type.type import Type
        is_ast_valid = (isinstance(last_arg, ast.Name)
                        or (isinstance(last_arg, ast.NameConstant) and args_types[-1] is Type.none))

        is_id_valid = (hasattr(last_arg, 'id')
                       and last_arg.id != args_types[-1].identifier
                       and last_arg.id != args_types[-1].raw_identifier
                       and isinstance(self.get_type(last_arg, use_metadata=True), MetaType))

        if not is_ast_valid or is_id_valid:
            # if the value is not the identifier of a type
            self._log_error(
                CompilerError.MismatchedTypes(
                    last_arg.lineno, last_arg.col_offset,
                    expected_type_id=type.__name__,
                    actual_type_id=args_types[-1].identifier
                ))
