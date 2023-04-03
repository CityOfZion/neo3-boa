import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from boa3.internal import constants
from boa3.internal.analyser.analyser import Analyser
from boa3.internal.compiler.compileroutput import CompilerOutput
from boa3.internal.model.event import Event
from boa3.internal.model.imports.importsymbol import BuiltinImport, Import
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo import to_hex_str
from boa3.internal.neo.contracts.neffile import NefFile


class FileGenerator:
    """
    This class is responsible for generating the files.
    """

    def __init__(self, compiler_result: CompilerOutput, analyser: Analyser, entry_file: str):
        import os
        self._metadata = analyser.metadata
        self._symbols: Dict[str, ISymbol] = analyser.symbol_table.copy()

        self._entry_file = entry_file
        self._entry_file_full_path = analyser.path.replace(os.sep, constants.PATH_SEPARATOR)

        self._files: List[str] = [self._entry_file_full_path]
        self._nef: NefFile = NefFile(compiler_result.bytecode,
                                     source=self._metadata.source,
                                     method_tokens=compiler_result.method_tokens)

        self.__all_imports: List[Import] = None
        self._all_methods: Dict[str, Method] = None
        self._all_static_vars: Dict[str, Variable] = None

    @property
    def _public_methods(self) -> Dict[str, Method]:
        """
        Gets a sublist of the symbols containing all public methods

        :return: a dictionary that maps each public method with its identifier
        """
        return {name: method for name, method in self._methods.items() if method.is_public}

    @property
    def _static_variables(self) -> Dict[str, Variable]:
        """
        Gets a sublist of the symbols containing all global variables

        :return: a dictionary that maps each global variable with its identifier
        """
        if self._all_static_vars is not None:
            return self._all_static_vars
        else:
            variables: Dict[Tuple[str, str], Variable] = {}
            imported_symbols: Dict[str, Import] = {}

            for name, symbol in self._symbols.items():
                if isinstance(symbol, Variable) and not symbol.is_reassigned:
                    variables[(self._entry_file, name)] = symbol
                elif isinstance(symbol, Import):
                    imported_symbols[symbol.origin] = symbol

            imported_to_map, imports_unique_ids = self._get_imports_unique_ids(imported_symbols,
                                                                               False,
                                                                               list(variables.values())
                                                                               )

            if imports_unique_ids[-1] != self._entry_file:
                # update entry file to be a unique name
                unique_id = imports_unique_ids[-1]
                variables = {(unique_id, method_name): method for (module_id, method_name), method in variables.items()}

            # include all user created methods in the list, even the methods that aren't imported in the entry file
            for index in range(len(imported_to_map)):
                module_full_path, module_import = list(imported_to_map.items())[index]
                module_id = imports_unique_ids[index]

                for name, symbol in module_import.all_symbols.items():
                    need_to_map = (isinstance(symbol, Variable)
                                   and not symbol.is_reassigned
                                   and symbol not in [variables for variables in variables.values()])
                    if need_to_map:
                        variables[(module_id, name)] = symbol

            if len(imports_unique_ids) > 1:
                self._all_static_vars = {f'{unique_id}{constants.VARIABLE_NAME_SEPARATOR}{var_id}': var
                                         for (unique_id, var_id), var in variables.items()}
            else:
                self._all_static_vars = {var_id: var
                                         for (unique_id, var_id), var in variables.items()}

            return self._all_static_vars

    @property
    def _methods(self) -> Dict[str, Method]:
        """
        Gets a sublist of the symbols containing all user methods

        :return: a dictionary that maps each method with its identifier
        """
        from boa3.internal.model.builtin.method import IBuiltinMethod
        return {name: method for name, method in self._symbols.items()
                if ((isinstance(method, Method) and method.defined_by_entry)
                    or (isinstance(method, IBuiltinMethod) and method.is_public)
                    )}

    @property
    def _methods_with_imports(self) -> Dict[Tuple[str, str], Method]:
        if self._all_methods is not None:
            return self._all_methods

        from boa3.internal.model.builtin.decorator.builtindecorator import IBuiltinCallable

        methods: Dict[Tuple[str, str], Method] = {}
        imported_symbols: Dict[str, Import] = {}

        for name, symbol in self._symbols.items():
            if symbol.defined_by_entry and isinstance(symbol, Method) and not isinstance(symbol, IBuiltinCallable):
                methods[(self._entry_file, name)] = symbol
            elif isinstance(symbol, Import):
                imported_symbols[symbol.origin] = symbol

        imported_to_map, imports_unique_ids = self._get_imports_unique_ids(imported_symbols,
                                                                           True,
                                                                           list(methods.values())
                                                                           )

        if imports_unique_ids[-1] != self._entry_file:
            # update entry file to be a unique name
            unique_id = imports_unique_ids[-1]
            methods = {(unique_id, method_name): method for (module_id, method_name), method in methods.items()}

        # include all user created methods in the list, even the methods that aren't imported in the entry file
        for index in range(len(imported_to_map)):
            module_full_path, module_import = list(imported_to_map.items())[index]
            module_id = imports_unique_ids[index]

            for name, symbol in module_import.all_symbols.items():
                if (isinstance(symbol, Method)
                        and not isinstance(symbol, IBuiltinCallable)
                        and symbol not in [method for method in methods.values()]):
                    methods[(module_id, name)] = symbol

        self._all_methods = methods
        return methods

    @property
    def _events(self) -> Dict[str, Event]:
        """
        Gets a sublist of the symbols containing all user events

        :return: a dictionary that maps each event with its identifier
        """
        events = set()
        for imported in self._all_imports:
            events.update([event for event in imported.all_symbols.values() if isinstance(event, Event)])
        events.update([event for event in self._symbols.values() if isinstance(event, Event)])

        return {event.name: event for event in events}

    @property
    def _all_imports(self) -> List[Import]:
        if self.__all_imports is not None:
            return self.__all_imports

        all_imports = [imported for imported in self._symbols.values()
                       if (isinstance(imported, Import)
                           and not isinstance(imported, BuiltinImport))]
        index = 0
        while index < len(all_imports):
            imported = all_imports[index]
            for inner in imported.all_symbols.values():
                if (isinstance(inner, Import)
                        and not isinstance(inner, BuiltinImport)
                        and inner not in all_imports):
                    all_imports.append(inner)
            index += 1

        self.__all_imports = list(reversed(all_imports))  # first positions are the most inner imports
        # using for instead a generator to keep the result determined
        for import_ in all_imports:
            if import_.origin not in self._files:
                self._files.append(import_.origin)
        return self.__all_imports

    # region NEF

    @property
    def _nef_hash(self) -> str:
        """
        Gets the string representation of the hash of the nef file

        :return: the hex string representation of the hash
        """
        return to_hex_str(self._nef.script_hash)

    def generate_nef_file(self) -> bytes:
        """
        Generates the .nef file

        :return: the resulting nef file as a byte array
        """
        return self._nef.serialize()

    # endregion

    # region Manifest

    def generate_manifest_file(self) -> bytes:
        """
        Generates the .manifest metadata file

        :return: the resulting manifest as a byte array
        """
        data: Dict[str, Any] = self._get_manifest_info()
        json_data: str = json.dumps(data, indent=4)
        return bytes(json_data, constants.ENCODING)

    def _get_manifest_info(self) -> Dict[str, Any]:
        """
        Gets the manifest information in a dictionary format

        :return: a dictionary with the manifest information
        """
        # TODO: fill the information of the manifest
        return {
            "name": self._get_name(),
            "groups": self._get_groups(),
            "abi": self._get_abi_info(),
            "permissions": self._get_permissions(),
            "trusts": self._metadata.trusts,
            "features": {},
            "supportedstandards": self._metadata.supported_standards,
            "extra": self._get_extras()
        }

    def _get_name(self) -> str:
        """
        Gets the name of the contract, if name wasn't specified it will be the file name.

        :return: the contract name
        """
        return self._metadata.name if self._metadata.name else self._entry_file

    def _get_permissions(self) -> List[Dict[str, Any]]:
        """
        Gets the permission information in a dictionary format, if _metadata._permissions is empty, then consider it
        with the import wildcard inside it.

        :return: a dictionary with the permission information
        """
        return self._metadata.permissions if self._metadata.permissions else [{"contract": constants.IMPORT_WILDCARD,
                                                                               "methods": constants.IMPORT_WILDCARD}]

    def _get_groups(self) -> List[Dict[str, Any]]:
        """
        Gets the group information in a dictionary format.

        :return: a dictionary with the groups information
        """
        return self._metadata.groups

    def _get_abi_info(self) -> Dict[str, Any]:
        """
        Gets the abi information in a dictionary format

        :return: a dictionary with the abi information
        """
        return {
            "methods": self._get_abi_methods(),
            "events": self._get_abi_events()
        }

    def _get_abi_methods(self) -> List[Dict[str, Any]]:
        """
        Gets the abi methods in a dictionary format

        :return: a dictionary with the abi methods
        """
        methods = []
        for method_id, method in self._public_methods.items():
            methods.append(self._construct_abi_method(method_id, method))
        return methods

    def _construct_abi_method(self, method_id: str, method: Method) -> Dict[str, Any]:
        from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping

        abi_method_name = method.external_name if isinstance(method.external_name, str) else method_id
        logging.getLogger(constants.BOA_LOGGING_NAME).info(f"'{abi_method_name}' method included in the manifest")

        method_abi = {
            "name": abi_method_name,
            "offset": (VMCodeMapping.instance().get_start_address(method.start_bytecode)
                       if method.start_bytecode is not None else 0),
            "parameters": [
                self._construct_abi_type_hint(arg.type, arg_id) for arg_id, arg in method.args.items()
            ],
            "safe": method.is_safe,
        }

        return_type_extension = self._construct_abi_type_hint(method.type, is_return_type=True)
        for return_type_name, return_type in return_type_extension.items():
            method_abi[return_type_name] = return_type

        return method_abi

    @staticmethod
    def _construct_abi_type_hint(var_type: IType, var_id: Optional[str] = None, is_return_type: bool = False) -> Optional[Dict[str, Any]]:
        """
        A recursive function that adds more details to some types on the manifest:
        - Arrays and Maps now have new keys to indicate the type of the items ('generic', 'generickey' and 'genericitem');
        - A String could have a 'hint' that it is an Address;
        - A Hash160 could have a 'hint' that it is a Scripthash or ScripthashLittleEndian;
        - A Hash256 could have a 'hint' that it is a BlockHash or TransactionId;
        - A StorageContext could have a 'hint' that it is a StorageContext or InteropInterface;
        - If the parameter or return is Optional, then the 'nullable' key will be added;
        - If the parameter or return is an Union, then the 'union' key will be added, with a list of types as value.
        """
        return_prefix = "return" if is_return_type else ""

        extended_type = {
            return_prefix + "type": var_type.abi_type
        }

        from boa3.internal.model.builtin.interop.interopinterfacetype import InteropInterfaceType
        from boa3.internal.model.type.annotation.uniontype import UnionType
        from boa3.internal.model.type.collection.sequence.mutable.listtype import ListType
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type
        from boa3.internal.model.type.collection.mapping.mutable.dicttype import DictType
        from boa3.internal.model.type.type import Type

        if isinstance(var_type, InteropInterfaceType):
            # Iterator or StorageContext is added as hint
            extended_type[return_prefix + "hint"] = var_type.raw_identifier

        # if it is a str, UInt160 or UInt256, then a type hint might be added
        elif any(
                isinstance(var_type, type(possible_type_hint)) and var_type.raw_identifier != possible_type_hint.raw_identifier
                for possible_type_hint in [Type.str, UInt160Type.build(), UInt256Type.build()]
        ):
            # Address, BlockHash, PublicKey, ScriptHash, ScriptHashLittleEndian or TransactionId is added as hint
            extended_type[return_prefix + "hint"] = var_type.raw_identifier

        # Calls itself to discover the types inside the Union/Optional
        elif isinstance(var_type, UnionType):

            from boa3.internal.model.type.annotation.optionaltype import OptionalType
            if isinstance(var_type, OptionalType):

                # if Optional is being used only with one type, e.g., Optional[Str], then don't consider it an Union
                if len(var_type.optional_types) == 1:
                    extended_type = FileGenerator._construct_abi_type_hint(var_type.optional_types[0],
                                                                           is_return_type=is_return_type)

                else:
                    extended_type[return_prefix + "union"] = [
                        FileGenerator._construct_abi_type_hint(union_type) for union_type in
                        var_type.optional_types
                    ]

                extended_type[return_prefix + "nullable"] = True

            else:
                extended_type[return_prefix + "union"] = [
                    FileGenerator._construct_abi_type_hint(union_type) for union_type in var_type.union_types
                ]

        # Calls itself to discover the types inside the List
        elif isinstance(var_type, ListType):
            extended_type[return_prefix + "generic"] = FileGenerator._construct_abi_type_hint(var_type.item_type)

        # Calls itself to discover the types inside the Dict
        elif isinstance(var_type, DictType):
            extended_type[return_prefix + "generickey"] = FileGenerator._construct_abi_type_hint(var_type.key_type)
            extended_type[return_prefix + "genericitem"] = FileGenerator._construct_abi_type_hint(var_type.item_type)

        if var_id is not None:
            extended_type[return_prefix + "name"] = var_id

        return extended_type

    def _get_abi_events(self) -> List[Dict[str, Any]]:
        """
        Gets the abi events in a dictionary format

        :return: a dictionary with the abi events
        """
        return [
            {
                "name": name,
                "parameters": [
                    {
                        "name": arg_id,
                        "type": arg.type.abi_type
                    } for arg_id, arg in event.args_to_generate.items()
                ],
            } for name, event in self._events.items() if event.is_called
        ]

    def _get_extras(self) -> Optional[Dict[str, Any]]:
        """
        Gets the abi information in a dictionary format

        :return: a dictionary with the abi information
        """
        extras = {}
        for key, value in self._metadata.extras.items():
            try:
                json.dumps(value)  # include only json like extras
                extras[key] = value
            except BaseException:
                continue

        return extras if len(extras) > 0 else None

    # endregion

    # region Debug Info

    def generate_nefdbgnfo_file(self) -> bytes:
        """
        Generates a debug map for NEO debugger

        :return: the resulting map as a byte array
        """
        data: Dict[str, Any] = self._get_debug_info()
        json_data: str = json.dumps(data, indent=4)
        return bytes(json_data, constants.ENCODING)

    def _get_debug_info(self) -> Dict[str, Any]:
        """
        Gets the debug information in a dictionary format

        :return: a dictionary with the debug information
        """
        return {
            "hash": self._nef_hash,
            "documents": self._files,
            "static-variables": self._get_debug_static_variables(),
            "methods": self._get_debug_methods(),
            "events": self._get_debug_events()
        }

    def _get_debug_methods(self) -> List[Dict[str, Any]]:
        """
        Gets the methods' debug information in a dictionary format

        :return: a dictionary with the methods' debug information
        """
        return [
            self._get_method_debug_info(module_id, method_id, method)
            for (module_id, method_id), method in self._methods_with_imports.items()
            if method.is_compiled
        ]

    def _get_method_debug_info(self, module_id: str, method_id: str, method: Method) -> Dict[str, Any]:
        from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
        from boa3.internal.neo.vm.type.AbiType import AbiType
        from boa3.internal.model.type.itype import IType
        return {
            "id": str(id(method)),
            "name": '{0},{1}'.format(module_id, method_id),
            "range": '{0}-{1}'.format(method.start_address, method.end_address),
            "params": [
                '{0},{1}'.format(name, var.type.abi_type) for name, var in method.args.items()
            ],
            "return": method.return_type.abi_type,
            "variables": [
                '{0},{1}'.format(name, var.type.abi_type if isinstance(var.type, IType) else AbiType.Any)
                for name, var in method.locals.items()
            ],
            "sequence-points": [
                '{0}[{1}]{2}:{3}-{4}:{5}'.format(VMCodeMapping.instance().get_start_address(instruction.code),
                                                 self._get_method_origin_index(method),
                                                 instruction.start_line, instruction.start_col,
                                                 instruction.end_line, instruction.end_col)
                for instruction in method.debug_map()
            ]
        }

    def _get_method_origin_index(self, method: Method) -> int:
        imported_files: List[Import] = [imported for imported in self._symbols.values()
                                        if (isinstance(imported, Import)
                                            and not isinstance(imported, BuiltinImport)
                                            and imported.origin is not None)]
        imported = None
        for file in imported_files:
            if method in file.all_symbols.values():
                imported = file
                break

        if imported is None:
            return 0
        else:
            if imported.origin not in self._files:
                self._files.append(imported.origin)
            return self._files.index(imported.origin)

    def _get_debug_events(self) -> List[Dict[str, Any]]:
        """
        Gets the events' debug information in a dictionary format

        :return: a dictionary with the event's debug information
        """
        return [
            {
                "id": str(id(event)),
                "name": ',{0}'.format(event_id),  # TODO: include module name
                "params": [
                    '{0},{1}'.format(name, var.type.abi_type) for name, var in event.args.items()
                ]
            } for event_id, event in self._events.items()
        ]

    def _get_debug_static_variables(self) -> List[str]:
        """
        Gets the static variables' debug information in a dictionary format

        :return: a dictionary with the event's debug information
        """
        from boa3.internal.model.type.itype import IType
        from boa3.internal.neo.vm.type.AbiType import AbiType

        static_variables = []

        for name, var in self._static_variables.items():
            var_unique_name = self._get_static_var_unique_name(name)
            var_type = var.type.abi_type if isinstance(var.type, IType) else AbiType.Any

            values = [var_unique_name, var_type.name]

            var_slot_index = self._get_static_var_slot_index(name)
            if isinstance(var_slot_index, int):
                values.append(str(var_slot_index))

            static_variables.append(
                constants.VARIABLE_NAME_SEPARATOR.join(values)
            )

        return static_variables

    # endregion

    def _get_static_var_unique_name(self, variable_id) -> str:
        imported_symbols: Dict[str, Import] = {}

        for name, symbol in self._symbols.items():
            if isinstance(symbol, Import):
                imported_symbols[symbol.origin] = symbol

        imported_to_map, imports_unique_ids = self._get_imports_unique_ids(imported_symbols,
                                                                           False,
                                                                           list(self._static_variables.values())
                                                                           )
        split_name = variable_id.split(constants.VARIABLE_NAME_SEPARATOR)
        if len(split_name) > 1:
            variable_original_id = split_name[-1]
            imported_id = constants.VARIABLE_NAME_SEPARATOR.join(split_name[:-1])
        else:
            variable_original_id = variable_id
            imported_id = None

        if isinstance(imported_id, str) and imported_id in imports_unique_ids:
            return '{0}.{1}'.format(imported_id, variable_original_id)

        if len(imported_to_map) <= 1:
            return variable_original_id

        for index, imported in enumerate(imported_symbols.values()):
            if isinstance(imported, Import) and variable_original_id in imported.all_symbols:
                if len(split_name) <= 1 or str(imported.ast.__hash__()) == split_name[0]:
                    return '{0}.{1}'.format(imports_unique_ids[index], variable_original_id)

        return '{0}.{1}'.format(imports_unique_ids[-1], variable_original_id)

    def _get_static_var_slot_index(self, variable_id) -> Optional[int]:
        module_globals = list(self._static_variables.keys())
        if variable_id in module_globals:
            return module_globals.index(variable_id)
        return None

    def _get_imports_unique_ids(self, imported_symbols: Dict[str, Import],
                                importing_methods: bool,
                                inner_imported_symbols: List[ISymbol] = None) -> Tuple[Dict[str, Import], List[str]]:
        if not isinstance(imported_symbols, dict):
            return {}, []
        if not isinstance(inner_imported_symbols, list):
            inner_imported_symbols = []

        from boa3.internal.model.builtin.builtincallable import IBuiltinCallable

        # must map all imports, including inner imports
        index = 0
        while index < len(imported_symbols):
            module_origin, imported = list(imported_symbols.items())[index]
            for name, inner_imported in imported.all_symbols.items():
                if isinstance(inner_imported, Import) and inner_imported.origin not in inner_imported_symbols:
                    imported_symbols[inner_imported.origin] = inner_imported
            index += 1

        # map the modules that have user modules not imported by the entry file
        imported_to_map: Dict[str, Import] = {}
        for name, imported in imported_symbols.items():
            if isinstance(imported, BuiltinImport):
                need_to_map = False
            else:
                need_to_map = any(not importing_methods  # is importing variables or is a method but not builtin
                                  or (((isinstance(symbol, Method) and not isinstance(symbol, IBuiltinCallable))
                                       or (isinstance(symbol, ClassType) and len(symbol.symbols) > 0)
                                       )
                                      and symbol not in inner_imported_symbols)
                                  for name, symbol in imported.all_symbols.items())
            if need_to_map:
                filtered_name = name.replace('.py', '').replace('/__init__', '')
                imported_to_map[filtered_name] = imported_symbols[name]
                if name not in self._files:
                    self._files.append(name)

        # change the full path names to unique small names
        imports_paths = list(imported_to_map)
        imports_paths.append(self._entry_file_full_path.replace('.py', '').replace('/__init__', ''))

        imports_unique_ids = []
        imports_duplicated_ids = []

        for index in range(len(imports_paths)):
            name = imports_paths[index]
            split_name = name.split(constants.PATH_SEPARATOR)
            index = -1
            short_name = split_name[index]
            while short_name in imports_duplicated_ids:
                index -= 1
                short_name = constants.ATTRIBUTE_NAME_SEPARATOR.join(split_name[index:])

            if short_name in imports_unique_ids:
                index_of_duplicated = imports_unique_ids.index(short_name)

                dup_split_name = imports_paths[index_of_duplicated].split(constants.PATH_SEPARATOR)
                dup_new_id = short_name
                dup_index = -len(imports_unique_ids[index].split(constants.ATTRIBUTE_NAME_SEPARATOR))

                while dup_new_id == short_name:
                    imports_duplicated_ids.append(short_name)
                    index -= 1
                    dup_index -= 1
                    short_name = constants.ATTRIBUTE_NAME_SEPARATOR.join(split_name[index:])
                    dup_new_id = constants.ATTRIBUTE_NAME_SEPARATOR.join(dup_split_name[dup_index:])

                imports_unique_ids[index_of_duplicated] = dup_new_id

            imports_unique_ids.append(short_name)

        return imported_to_map, imports_unique_ids
