import ast
import logging
import os
from abc import ABC
from collections.abc import Sequence
from inspect import isclass
from typing import Any

from boa3.internal import constants
from boa3.internal.exception.CompilerError import CompilerError, InternalError, UnresolvedReference
from boa3.internal.exception.CompilerWarning import CompilerWarning
from boa3.internal.model.attribute import Attribute
from boa3.internal.model.expression import IExpression
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.operation.operation import IOperation
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.annotation.metatype import MetaType
from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.model.type.type import IType, Type
from boa3.internal.model.type.typeutils import TypeUtils


class IAstAnalyser(ABC, ast.NodeVisitor):
    """
    An interface for the analysers that walk the Python abstract syntax tree

    :ivar errors: a list that contains all the errors raised by the compiler. Empty by default.
    :ivar warnings: a list that contains all the warnings found by the compiler. Empty by default.
    """

    def __init__(self, ast_tree: ast.AST, filename: str = None, root_folder: str = None,
                 log: bool = False, fail_fast: bool = True):
        self.errors: list[CompilerError] = []
        self.warnings: list[CompilerWarning] = []

        self.filename: str | None = filename
        if not isinstance(root_folder, str) or not os.path.isdir(root_folder):
            root_folder = (os.path.dirname(os.path.abspath(filename))
                           if isinstance(filename, str) and os.path.isfile(filename)
                           else os.path.abspath(os.path.curdir))
        self.root_folder: str = root_folder
        self._log: bool = log
        self._fail_fast: bool = fail_fast

        self._tree: ast.AST = ast_tree
        self.symbols: dict[str, ISymbol] = {}

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def _log_error(self, error: CompilerError):
        if self._fail_fast and len(self.errors) > 0:
            raise error

        if error.filepath is None:
            error.filepath = self.filename
        if not any(err == error for err in self.errors):
            # don't include duplicated errors
            self.errors.append(error)
            if self._log:
                logging.getLogger(constants.BOA_LOGGING_NAME).error(error)

        if self._fail_fast:
            raise error

    def _log_warning(self, warning: CompilerWarning):
        if warning.filepath is None:
            warning.filepath = self.filename
        if not any(warn == warning for warn in self.warnings):
            # don't include duplicated warnings
            self.warnings.append(warning)
            if self._log:
                logging.getLogger(constants.BOA_LOGGING_NAME).warning(warning)

    def _log_info(self, info_message: str, log_filename: bool = True):
        if self._log:
            if log_filename and self.filename:
                formatted_message = f'{info_message} <{self.filename}>'
            else:
                formatted_message = info_message

            logging.getLogger(constants.BOA_LOGGING_NAME).info(formatted_message)

    def analyse_visit(self, node: ast.AST) -> Any:
        try:
            return self.visit(node)
        except CompilerError:
            # stops the analyser if fail fast is activated
            pass

    def visit(self, node: ast.AST) -> Any:
        try:
            return super().visit(node)
        except CompilerError as error:
            self._log_error(error)
        except CompilerWarning as warning:
            self._log_warning(warning)
        except KeyboardInterrupt as interrupt:
            raise interrupt
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
                value = self.get_symbol(fun_rtype_id, origin_node=value)
                if isinstance(value, IType) and not isinstance(value, MetaType):
                    value = TypeUtils.type.build(value) if use_metatype else value
            else:
                value = fun_rtype_id

        if isinstance(value, Attribute):
            if ((isinstance(value.attr_symbol, IExpression) and isinstance(value.attr_symbol.type, ClassType))
                    or (isinstance(value.attr_symbol, IType))):
                value = value.attr_symbol
            elif isinstance(value.type, IType):
                value = value.type

        if isinstance(value, IType):
            final_type = value
        elif isinstance(value, IExpression):
            final_type = value.type
        elif isinstance(value, IOperation):
            final_type = value.result
        else:
            final_type = Type.get_type(value)

        if isinstance(final_type, MetaType) and not use_metatype:
            return final_type.meta_type
        else:
            return final_type

    def get_symbol(self, symbol_id: str,
                   is_internal: bool = False,
                   check_raw_id: bool = False,
                   origin_node: ast.AST = None) -> ISymbol | None:
        """
        Tries to get the symbol by its id name

        :param symbol_id: the id name of the symbol
        :return: the symbol if found. None otherwise.
        :rtype: ISymbol or None
        """
        if symbol_id in self.symbols:
            # the symbol exists in the global scope
            return self.symbols[symbol_id]

        if check_raw_id:
            found_symbol = self._search_by_raw_id(symbol_id, list(self.symbols.values()))
            if found_symbol is not None:
                # the symbol exists in the global scope, but with an alias different from the original name
                return found_symbol

        if is_internal:
            from boa3.internal.model import imports
            found_symbol = imports.compilerbuiltin.get_internal_symbol(symbol_id)
            if isinstance(found_symbol, ISymbol):
                return found_symbol

        # the symbol may be a built in. If not, returns None
        from boa3.internal.model.builtin.builtin import Builtin
        found_symbol = Builtin.get_symbol(symbol_id)

        if found_symbol is None and isinstance(symbol_id, str) and self.is_exception(symbol_id):
            found_symbol = Builtin.Exception.return_type

        if origin_node is not None and found_symbol is None:
            self._log_error(
                UnresolvedReference(
                    line=origin_node.lineno,
                    col=origin_node.col_offset,
                    symbol_id=symbol_id
                )
            )

        return found_symbol

    def _search_by_raw_id(self, symbol_id: str, symbols: Sequence[ISymbol]) -> ISymbol | None:
        for symbol in symbols:
            if isinstance(symbol, IdentifiedSymbol) and symbol.identifier == symbol_id:
                return symbol

        return None

    def is_exception(self, symbol_id: str) -> bool:
        global_symbols = globals()
        if symbol_id in global_symbols or symbol_id in global_symbols['__builtins__']:
            symbol = (global_symbols[symbol_id]
                      if symbol_id in global_symbols
                      else global_symbols['__builtins__'][symbol_id])
            if isclass(symbol) and issubclass(symbol, BaseException):
                return True
        return False

    def is_implemented_class_type(self, symbol) -> bool:
        if not isinstance(symbol, ClassType):
            return False

        from boa3.internal.model.type.classes.pythonclass import PythonClass
        from boa3.internal.model.builtin.interop.interopinterfacetype import InteropInterfaceType

        return not isinstance(symbol, PythonClass) or isinstance(symbol, InteropInterfaceType)

    def parse_to_node(self, expression: str, origin: ast.AST = None) -> ast.AST | Sequence[ast.AST]:
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

        for attr in node.__dict__:
            clone.__setattr__(attr, node.__getattribute__(attr))

        return clone
