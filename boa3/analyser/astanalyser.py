import ast
import logging
from abc import ABC
from inspect import isclass
from typing import Any, Dict, List, Optional, Sequence, Union

from boa3.exception.CompilerError import CompilerError, InternalError
from boa3.exception.CompilerWarning import CompilerWarning
from boa3.model.attribute import Attribute
from boa3.model.expression import IExpression
from boa3.model.operation.operation import IOperation
from boa3.model.symbol import ISymbol
from boa3.model.type.annotation.metatype import MetaType
from boa3.model.type.classtype import ClassType
from boa3.model.type.type import IType, Type
from boa3.model.type.typeutils import TypeUtils


class IAstAnalyser(ABC, ast.NodeVisitor):
    """
    An interface for the analysers that walk the Python abstract syntax tree

    :ivar errors: a list that contains all the errors raised by the compiler. Empty by default.
    :ivar warnings: a list that contains all the warnings found by the compiler. Empty by default.
    """

    def __init__(self, ast_tree: ast.AST, filename: str = None, log: bool = False):
        self.errors: List[CompilerError] = []
        self.warnings: List[CompilerWarning] = []

        self.filename: Optional[str] = filename
        self._log: bool = log

        self._tree: ast.AST = ast_tree
        self.symbols: Dict[str, ISymbol] = {}

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def _log_error(self, error: CompilerError):
        if not any(err == error for err in self.errors):
            # don't include duplicated errors
            self.errors.append(error)
            if self._log:
                logging.error(error)

    def _log_warning(self, warning: CompilerWarning):
        if not any(warn == warning for warn in self.warnings):
            # don't include duplicated warnings
            self.warnings.append(warning)
            if self._log:
                logging.warning(warning)

    def visit(self, node: ast.AST) -> Any:
        try:
            return super().visit(node)
        except CompilerError as error:
            self._log_error(error)
        except CompilerWarning as warning:
            self._log_warning(warning)
        except BaseException as exception:
            if hasattr(node, 'lineno'):
                self._log_error(
                    InternalError(line=node.lineno,
                                  col=node.col_offset,
                                  raised_exception=exception)
                )

    def get_type(self, value: Any, use_metatype: bool = False) -> IType:
        """
        Returns the type of the given value.

        :param value: value to get the type
        :param use_metatype: whether it should return `Type.type` if the value is an IType implementation.
        :return: Returns the :class:`IType` of the the type of the value. `Type.none` by default.
        """
        # visits if it is a node
        if isinstance(value, ast.AST):
            fun_rtype_id: Any = ast.NodeVisitor.visit(self, value)
            if isinstance(fun_rtype_id, ast.Name):
                fun_rtype_id = fun_rtype_id.id

            if isinstance(fun_rtype_id, str) and not isinstance(value, ast.Str):
                value = self.get_symbol(fun_rtype_id)
                if isinstance(value, IType) and not isinstance(value, MetaType):
                    value = TypeUtils.type.build(value) if use_metatype else value
            else:
                value = fun_rtype_id

        if (isinstance(value, Attribute)
                and isinstance(value.attr_symbol, IExpression)
                and isinstance(value.attr_symbol.type, ClassType)):
            value = value.attr_symbol

        if isinstance(value, IType):
            final_type = value
        elif isinstance(value, IExpression):
            final_type = value.type
        elif isinstance(value, IOperation):
            final_type = value.result
        else:
            final_type = Type.get_type(value)

        if isinstance(final_type, MetaType):
            print()
        if isinstance(final_type, MetaType) and not use_metatype:
            return final_type.meta_type
        else:
            return final_type

    def get_symbol(self, symbol_id: str, is_internal: bool = False) -> Optional[ISymbol]:
        """
        Tries to get the symbol by its id name

        :param symbol_id: the id name of the symbol
        :return: the symbol if found. None otherwise.
        :rtype: ISymbol or None
        """
        if symbol_id in self.symbols:
            # the symbol exists in the global scope
            return self.symbols[symbol_id]

        if is_internal:
            from boa3.model.importsymbol import Import
            imports = [symbol for symbol in self.symbols.values() if isinstance(symbol, Import)]
            for package in imports:
                if symbol_id in package.all_symbols:
                    return package.all_symbols[symbol_id]

        # the symbol may be a built in. If not, returns None
        from boa3.model.builtin.builtin import Builtin
        found_symbol = Builtin.get_symbol(symbol_id)

        if found_symbol is None and isinstance(symbol_id, str) and self.is_exception(symbol_id):
            found_symbol = Builtin.Exception.return_type
        return found_symbol

    def is_exception(self, symbol_id: str) -> bool:
        global_symbols = globals()
        if symbol_id in global_symbols or symbol_id in global_symbols['__builtins__']:
            symbol = (global_symbols[symbol_id]
                      if symbol_id in global_symbols
                      else global_symbols['__builtins__'][symbol_id])
            if isclass(symbol) and issubclass(symbol, BaseException):
                return True
        return False

    def parse_to_node(self, expression: str, origin: ast.AST = None) -> Union[ast.AST, Sequence[ast.AST]]:
        """
        Parses an expression to an ast.

        :param expression: string expression to be parsed
        :param origin: an existing ast. If not None, the parsed node will have the same location of origin.
        :return: the parsed node
        :rtype: ast.AST or Sequence[ast.AST]
        """
        node = ast.parse(expression, filename='<{0}>'.format(type(self).__name__))
        if origin is not None:
            self.update_line_and_col(node, origin)

        # get the expression instead of the default root node
        if hasattr(node, 'body'):
            node = node.body
        elif hasattr(node, 'argtypes'):
            node = node.argtypes

        if isinstance(node, list) and len(node) == 1:
            # the parsed node has a list of expression and only one expression is found
            result = node[0]
        else:
            result = node

        if isinstance(result, ast.Expr):
            # an expr node encapsulates another node in its value field.
            result = result.value
        return result

    def update_line_and_col(self, target: ast.AST, origin: ast.AST):
        """
        Updates the position of a node and its child nodes

        :param target: the node that will have its position updated
        :param origin: the node with the desired position
        """
        ast.copy_location(target, origin)
        for field, value in ast.iter_fields(target):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.update_line_and_col(item, origin)
            elif isinstance(value, ast.AST):
                self.update_line_and_col(value, origin)
        ast.fix_missing_locations(target)

    def clone(self, node: ast.AST) -> ast.AST:
        """
        Clones an AST node

        :param node: node to be cloned
        :return:
        """
        clone: ast.AST = node.__class__()
        clone._attributes = node._attributes
        clone._fields = node._fields

        for attr in node._attributes + node._fields:
            clone.__setattr__(attr, node.__getattribute__(attr))

        return clone
