import ast
import importlib.util
import os
import sys

from boa3.internal import constants
from boa3.internal.analyser.astanalyser import IAstAnalyser
from boa3.internal.model import imports
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.type import Type


class ImportAnalyser(IAstAnalyser):

    def __init__(self, import_target: str, root_folder: str,
                 importer_file: str | None = None,
                 import_stack: list[str] = None,
                 already_imported_modules: dict = None,
                 log: bool = False,
                 fail_fast: bool = True,
                 get_entry: bool = False):

        self.can_be_imported: bool = False
        self.is_builtin_import: bool = False
        self.is_namespace_package: bool = False
        self.recursive_import: bool = False
        self._import_identifier: str = import_target

        self._get_from_entry: bool = get_entry and (os.path.isfile(import_target) or os.path.isdir(import_target))

        from boa3.internal.model.imports.package import Package
        self._package: Package | None = None
        from boa3.internal.analyser.analyser import Analyser
        self._imported_files: dict[str, Analyser] = (already_imported_modules
                                                     if isinstance(already_imported_modules, dict)
                                                     else {})
        self._import_stack: list[str] = import_stack if isinstance(import_stack, list) else []
        self.analyser: Analyser = None  # set if the import is successful
        self._submodule_search_locations = None

        if isinstance(root_folder, str):
            if os.path.isfile(root_folder):
                root = os.path.dirname(root_folder)
            elif os.path.isdir(root_folder):
                root = root_folder
            else:
                root = os.path.dirname(importer_file)
        else:
            root = os.path.dirname(importer_file)

        super().__init__(ast.Module(body=[]), root_folder=root, log=log, fail_fast=fail_fast)

        if self._get_from_entry:
            self.path: str = import_target.replace(os.sep, constants.PATH_SEPARATOR)
            self._find_package(import_target, importer_file)
            return

        importer_file_dir = os.path.dirname(importer_file)
        sys.path.insert(0, self.root_folder)
        sys.path.insert(1, importer_file_dir)
        try:
            import_spec = importlib.util.find_spec(import_target)
            module_origin: str = import_spec.origin
        except BaseException:
            return
        finally:
            sys.path.remove(importer_file_dir)
            sys.path.remove(self.root_folder)

        self._importer_file = importer_file
        is_importing_a_module = module_origin is not None

        if not is_importing_a_module:
            self.is_namespace_package = True
            if import_spec.submodule_search_locations is None:
                return

            # submodule_search_locations type doesn't support indexing, so we need to iterate to get the first
            for module_ in import_spec.submodule_search_locations:
                module_origin: str = module_  # + "\\" + names[0] + '.py'
                break

            # if the origin is still not set, there's nothing to import
            if module_origin is None:
                return

        path: list[str] = module_origin.split(os.sep)
        self.filename = path[-1]
        self._submodule_search_locations = import_spec.submodule_search_locations
        self.path: str = module_origin.replace(os.sep, constants.PATH_SEPARATOR)

        self._find_package(module_origin, importer_file)

    @property
    def tree(self) -> ast.AST:
        return self._tree

    @property
    def is_import_deprecated(self) -> bool:
        return self._package.is_deprecated if self._package is not None else False

    def export_symbols(self, identifiers: list[str] = None) -> dict[str, ISymbol]:
        """
        Gets a dictionary that maps each exported symbol with its identifier

        :param identifiers: list of identifiers of the imported symbols
        :return:
        """
        if identifiers is None:
            identifiers = list([name for name, symbol in self.symbols.items() if symbol is not None])
        if not self.can_be_imported or not isinstance(identifiers, (list, str)):
            return {}

        if isinstance(identifiers, str):
            identifiers = [identifiers]

        if constants.IMPORT_WILDCARD in identifiers:
            symbols = self.symbols.copy()
        else:
            symbols = {symbol_id: symbol for symbol_id, symbol in self.symbols.items()
                       if symbol_id in identifiers and symbol is not None}
        return symbols

    def update_external_analysed_files(self, external_files: dict):
        if self.can_be_imported and self.path in self._imported_files and self.path not in external_files:
            external_files[self.path] = self._imported_files[self.path]

        for path, analyser in self._imported_files.items():
            if path not in external_files and analyser.is_analysed:
                external_files[path] = analyser

    def _find_package(self, module_origin: str, origin_file: str | None = None):
        path: list[str] = module_origin.split(os.sep)

        package = imports.compilerbuiltin.get_package(self._import_identifier)
        if hasattr(package, 'symbols'):
            if hasattr(package, 'inner_packages'):
                # when have symbol and packages with the same id, prioritize symbol
                self.symbols: dict[str, ISymbol] = package.inner_packages
                self.symbols.update(package.symbols)
            else:
                self.symbols = package.symbols

            self._package = package
            self.can_be_imported = True
            self.is_builtin_import = True
            return

        def is_boa_package() -> bool:
            common_path = os.path.commonpath([self.path, constants.BOA_PACKAGE_PATH])
            if common_path == constants.BOA_PACKAGE_PATH:
                return True
            if 'boa3' not in path:
                return False

            boa_path = path[path.index('boa3'):]
            return len(boa_path) > 1 and boa_path[1] in ('builtin', 'sc')

        if not is_boa_package():
            # doesn't analyse boa3.builtin packages that aren't included in the imports.compilerbuiltin as an user module
            import re

            inside_python_folder = any(re.search(r'python(\d\.?)*', folder.lower()) for folder in path)
            updated_tree = None

            if not (inside_python_folder and 'lib' in path):
                # check circular imports to avoid recursions inside the compiler
                if self.path in self._import_stack:
                    self.recursive_import = True
                    return

                # only user modules and typing lib imports are implemented
                try:
                    if self.path in self._imported_files:
                        analyser = self._imported_files[self.path]
                    else:
                        from boa3.internal.analyser.analyser import Analyser
                        origin = origin_file.replace(os.sep, constants.PATH_SEPARATOR)
                        files = self._import_stack
                        files.append(origin)
                        if self.is_namespace_package:
                            analyser = Analyser(self.tree, module_origin, self.root_folder, log=self._log,
                                                env=self.analyser.env if hasattr(self.analyser, 'env') else None
                                                )
                            if self._include_inner_packages(analyser):
                                analyser.is_analysed = True
                                self._imported_files[self.path] = analyser
                        else:
                            analyser = Analyser.analyse(module_origin, root=self.root_folder,
                                                        imported_files=self._imported_files,
                                                        import_stack=files,
                                                        log=self._log, fail_fast=True)

                            if self._fail_fast and len(analyser.errors) > 0:
                                raise analyser.errors[0]
                            self._include_inner_packages(analyser)

                        if analyser.is_analysed:
                            self._imported_files[self.path] = analyser

                    # include only imported symbols
                    if analyser.is_analysed:
                        for symbol_id, symbol in analyser.symbol_table.items():
                            if symbol_id not in Type.all_types():
                                if not self._get_from_entry:
                                    symbol.defined_by_entry = False
                                self.symbols[symbol_id] = symbol

                    self.errors.extend(analyser.errors)
                    self.warnings.extend(analyser.warnings)

                    updated_tree = analyser.ast_tree
                    self.analyser = analyser
                    self.can_be_imported = analyser.is_analysed
                except FileNotFoundError:
                    self.can_be_imported = False

                if updated_tree is not None:
                    self._tree = updated_tree

    def _include_inner_packages(self, analyser) -> bool:
        if self.path.endswith('.py') and self.filename != f'{constants.INIT_METHOD_ID}.py':
            return False

        import pkgutil
        from boa3.internal.model.imports.importsymbol import Import
        from boa3.internal.model.imports.package import Package

        inner_packages_have_errors = False
        modules = {}
        for importer, modname, is_pkg in pkgutil.iter_modules(self._submodule_search_locations):
            mod_target = self._import_identifier + constants.ATTRIBUTE_NAME_SEPARATOR + modname
            import_analyser = ImportAnalyser(mod_target, self.root_folder,
                                             importer_file=self._importer_file,
                                             import_stack=self._import_stack,
                                             already_imported_modules=self._imported_files,
                                             log=self._log)

            if not inner_packages_have_errors and not import_analyser.can_be_imported:
                inner_packages_have_errors = True

            imported = Package(identifier=modname,
                               other_symbols=import_analyser.symbols,
                               import_origin=Import(import_analyser.path,
                                                    import_analyser._tree,
                                                    import_analyser))
            modules[modname] = imported

        if len(modules) > 0 and hasattr(analyser, 'symbol_table') and isinstance(analyser.symbol_table, dict):
            analyser.symbol_table.update(modules)

        return not inner_packages_have_errors
