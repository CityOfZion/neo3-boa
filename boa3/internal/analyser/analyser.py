import ast
from typing import Self

from boa3.builtin.compile_time import NeoMetadata
from boa3.internal import constants
from boa3.internal.analyser.astanalyser import IAstAnalyser
from boa3.internal.analyser.astoptimizer import AstOptimizer
from boa3.internal.analyser.constructanalyser import ConstructAnalyser
from boa3.internal.analyser.moduleanalyser import ModuleAnalyser
from boa3.internal.analyser.supportedstandard.standardanalyser import StandardAnalyser
from boa3.internal.analyser.typeanalyser import TypeAnalyser
from boa3.internal.compiler.compiledmetadata import CompiledMetadata
from boa3.internal.exception.CompilerError import CompilerError
from boa3.internal.exception.CompilerWarning import CompilerWarning
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.type import Type


class Analyser:
    """
    This class is responsible for the semantic analysis of the code

    :ivar symbol_table: a dictionary used to store the identifiers
    """

    def __init__(self, ast_tree: ast.AST, path: str = None, project_root: str = None,
                 env: str = None, log: bool = False, fail_fast: bool = False):
        self.symbol_table: dict[str, ISymbol] = {}

        self.ast_tree: ast.AST = ast_tree
        self.metadata: NeoMetadata = NeoMetadata()
        self.is_analysed: bool = False
        self._log: bool = log
        self._fail_fast: bool = fail_fast
        self._env: str = env if env is not None else constants.DEFAULT_CONTRACT_ENVIRONMENT

        self.__include_builtins_symbols()
        self._errors = []
        self._warnings = []
        self._imported_files: dict[str, Analyser] = {}
        self._included_imported_files: bool = False

        import os
        self.path: str = path
        self.filename: str = path if path is None else os.path.realpath(path)

        if project_root is not None:
            if not os.path.exists(project_root):
                project_root = os.path.abspath(f'{os.path.curdir}{os.path.sep}{project_root}')

            if os.path.isfile(project_root):
                project_root = os.path.dirname(os.path.abspath(project_root))

        self.root: str = (os.path.realpath(project_root)
                          if project_root is not None and os.path.isdir(project_root)
                          else path)

    @classmethod
    def analyse(
            cls,
            path: str,
            log: bool = False,
            fail_fast: bool = False,
            imported_files: dict[str, Self] | None = None,
            import_stack: list[str] | None = None,
            root: str = None,
            env: str = None,
            compiler_entry: bool = False
    ) -> Self:
        """
        Analyses the syntax of the Python code

        :param path: the path of the Python file
        :param log: if compiler errors should be logged.
        :param fail_fast: if should stop compilation on first error found.
        :param import_stack: a list that represents the current import stack if it's from an import.
                             If it's not triggered by an import, must be None.
        :param imported_files: a dict that maps the paths of the files that were analysed if it's from an import.
                               If it's not triggered by an import, must be None.
        :param root: the path of the project root that the current smart contract is part of.
        :param env: specific environment id to compile.
        :param compiler_entry: Whether this is the entry compiler analyser. False by default.
        :return: a boolean value that represents if the analysis was successful
        :rtype: Analyser
        """
        with open(path, 'rb') as source:
            ast_tree = ast.parse(source.read())

        analyser = Analyser(ast_tree, path, root if isinstance(root, str) else path, env, log, fail_fast)
        CompiledMetadata.set_current_metadata(analyser.metadata)

        if compiler_entry:
            from boa3.internal.model.imports.compilerbuiltin import CompilerBuiltin
            CompilerBuiltin.update_with_analyser(analyser)

        # fill symbol table
        if not analyser.__analyse_modules(imported_files, import_stack):
            return analyser
        analyser.__pre_execute()

        # check if standards are correctly implemented
        if not analyser.__check_standards():
            return analyser
        # check is the types are correct
        if not analyser.__check_types():
            return analyser

        analyser.__pos_execute()
        analyser.is_analysed = True

        return analyser

    @property
    def errors(self) -> list[CompilerError]:
        return self._errors.copy()

    @property
    def warnings(self) -> list[CompilerWarning]:
        return self._warnings.copy()

    @property
    def env(self) -> str:
        return self._env

    def copy(self) -> Self:
        copied = Analyser(ast_tree=self.ast_tree, path=self.path, project_root=self.root,
                          env=self._env, log=self._log, fail_fast=self._fail_fast)

        copied.metadata = self.metadata
        copied.is_analysed = self.is_analysed
        copied.symbol_table = self.symbol_table.copy()
        copied.filename = self.filename
        copied._imported_files = self._imported_files.copy()
        copied._included_imported_files = self._included_imported_files

        return copied

    def __include_builtins_symbols(self):
        """
        Include the Python builtins in the global symbol table
        """
        self.symbol_table.update(Type.builtin_types())

    def __check_types(self) -> bool:
        """
        Performs the type checking

        :return: a boolean value that represents if the analysis was successful
        """
        type_analyser = TypeAnalyser(self, self.symbol_table, log=self._log, fail_fast=self._fail_fast)
        self._update_logs(type_analyser)
        return not type_analyser.has_errors

    def __analyse_modules(self,
                          imported_files: dict[str, Self] | None = None,
                          import_stack: list[str] | None = None) -> bool:
        """
        Validates the symbols and constructs the symbol table of the ast tree

        :return: a boolean value that represents if the analysis was successful
        """
        current_metadata = self.metadata
        module_analyser = ModuleAnalyser(self, self.symbol_table,
                                         log=self._log,
                                         fail_fast=self._fail_fast,
                                         filename=self.filename,
                                         root_folder=self.root,
                                         analysed_files=imported_files,
                                         import_stack=import_stack)
        self.symbol_table.update(module_analyser.global_symbols)
        self.ast_tree.body.extend(module_analyser.imported_nodes)
        self._update_logs(module_analyser)
        self._imported_files = module_analyser.analysed_files.copy()

        if self.metadata != current_metadata:
            CompiledMetadata.set_current_metadata(self.metadata)

        return not module_analyser.has_errors

    def __check_standards(self) -> bool:
        """
        Verify if the standards included in the metadata are fully implemented

        :return: a boolean value that represents if the analysis was successful
        """
        standards_analyser = StandardAnalyser(self, self.symbol_table, log=self._log, fail_fast=self._fail_fast)
        self._update_logs(standards_analyser)
        return not standards_analyser.has_errors

    def _update_logs(self, analyser: IAstAnalyser):
        self._errors.extend(analyser.errors)
        self._warnings.extend(analyser.warnings)

    def __pre_execute(self):
        """
        Pre executes the instructions of the ast for optimization
        """
        self.ast_tree = ConstructAnalyser(self, self.ast_tree, self.symbol_table,
                                          log=self._log, fail_fast=self._fail_fast
                                          ).tree

    def __pos_execute(self):
        """
        Tries to optimize the ast after validations
        """
        optimizer = AstOptimizer(self, log=self._log, fail_fast=self._fail_fast)
        self._update_logs(optimizer)

    def update_symbol_table(self, symbol_table: dict[str, ISymbol]):
        for symbol_id, symbol in symbol_table.items():
            if (hasattr(symbol, 'origin')
                    and hasattr(symbol.origin, 'origin')
                    and isinstance(symbol.origin.origin, ast.AST)
                    and len(symbol_id.split(constants.VARIABLE_NAME_SEPARATOR)) <= 1):

                if symbol_id in self.symbol_table:
                    self.symbol_table.pop(symbol_id)

                origin_hash = symbol.origin.origin.__hash__()
                unique_id = '{0}{2}{1}'.format(origin_hash, symbol_id, constants.VARIABLE_NAME_SEPARATOR)
            else:
                unique_id = symbol_id

            from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
            from boa3.internal.model.type.classes.userclass import UserClass
            if not isinstance(symbol, IdentifiedSymbol) or isinstance(symbol, UserClass):
                if unique_id not in self.symbol_table:
                    self.symbol_table[unique_id] = symbol

    def update_symbol_table_with_imports(self):
        if self._included_imported_files:
            return

        import os
        from boa3.internal.analyser.importanalyser import ImportAnalyser
        from boa3.internal.model.imports.importsymbol import Import

        imports = self._imported_files.copy()
        paths_already_imported = [imported.origin for imported in self.symbol_table.values()
                                  if isinstance(imported, Import) and isinstance(imported.origin, str)]
        if isinstance(self.path, str):
            paths_already_imported.append(self.path.replace(os.path.sep, constants.PATH_SEPARATOR))

        for file_path, analyser in imports.items():
            if file_path not in paths_already_imported:
                import_analyser = ImportAnalyser(file_path, self.root,
                                                 already_imported_modules=imports,
                                                 log=False, fail_fast=self._fail_fast,
                                                 get_entry=True)
                import_symbol = Import(file_path, analyser.ast_tree, import_analyser, {})
                self.symbol_table[file_path] = import_symbol

        self._included_imported_files = True

    def get_imports(self) -> list[Self]:
        return list(self._imported_files.values())
