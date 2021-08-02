import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from boa3 import constants
from boa3.analyser.analyser import Analyser
from boa3.constants import ENCODING
from boa3.model.event import Event
from boa3.model.imports.importsymbol import Import
from boa3.model.method import Method
from boa3.model.symbol import ISymbol
from boa3.model.variable import Variable
from boa3.neo import to_hex_str
from boa3.neo.contracts.neffile import NefFile


class FileGenerator:
    """
    This class is responsible for generating the files.
    """

    def __init__(self, bytecode: bytes, analyser: Analyser, entry_file: str):
        import os
        self._metadata = analyser.metadata
        self._symbols: Dict[str, ISymbol] = analyser.symbol_table

        self._entry_file = entry_file
        self._entry_file_full_path = analyser.path.replace(os.sep, '/')

        self._files: List[str] = [self._entry_file_full_path]
        self._nef: NefFile = NefFile(bytecode)

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
        return {name: variable for name, variable in self._symbols.items()
                if isinstance(variable, Variable) and not variable.is_reassigned}

    @property
    def _methods(self) -> Dict[str, Method]:
        """
        Gets a sublist of the symbols containing all user methods

        :return: a dictionary that maps each method with its identifier
        """
        from boa3.model.builtin.method import IBuiltinMethod
        return {name: method for name, method in self._symbols.items()
                if ((isinstance(method, Method) and method.defined_by_entry)
                    or (isinstance(method, IBuiltinMethod) and method.is_public)
                    )}

    @property
    def _methods_with_imports(self) -> Dict[Tuple[str, str], Method]:
        from boa3.model.builtin.decorator.builtindecorator import IBuiltinCallable

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

        return methods

    @property
    def _events(self) -> Dict[str, Event]:
        """
        Gets a sublist of the symbols containing all user events

        :return: a dictionary that maps each event with its identifier
        """
        return {event.name: event for event in self._symbols.values() if isinstance(event, Event)}

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
        return bytes(json_data, ENCODING)

    def _get_manifest_info(self) -> Dict[str, Any]:
        """
        Gets the manifest information in a dictionary format

        :return: a dictionary with the manifest information
        """
        # TODO: fill the information of the manifest
        return {
            "name": self._entry_file,
            "groups": [],
            "abi": self._get_abi_info(),
            "permissions": [
                {
                    "contract": "*",
                    "methods": "*"
                }
            ],
            "trusts": [],
            "features": {},
            "supportedstandards": self._metadata.supported_standards,
            "extra": self._metadata.extra if len(self._metadata.extra) > 0 else None
        }

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
            logging.info("'{0}' method included in the ABI".format(method_id))
            methods.append(self._construct_abi_method(method_id, method))
        return methods

    def _construct_abi_method(self, method_id: str, method: Method) -> Dict[str, Any]:
        from boa3.compiler.codegenerator.vmcodemapping import VMCodeMapping
        return {
            "name": method_id,
            "offset": (VMCodeMapping.instance().get_start_address(method.start_bytecode)
                       if method.start_bytecode is not None else 0),
            "parameters": [
                {
                    "name": arg_id,
                    "type": arg.type.abi_type
                } for arg_id, arg in method.args.items()
            ],
            "returntype": method.type.abi_type,
            "safe": False
        }

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
            } for name, event in self._events.items()
        ]

    # endregion

    # region Debug Info

    def generate_nefdbgnfo_file(self) -> bytes:
        """
        Generates a debug map for NEO debugger

        :return: the resulting map as a byte array
        """
        data: Dict[str, Any] = self._get_debug_info()
        json_data: str = json.dumps(data, indent=4)
        return bytes(json_data, ENCODING)

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
        ]

    def _get_method_debug_info(self, module_id: str, method_id: str, method: Method) -> Dict[str, Any]:
        from boa3.compiler.codegenerator.vmcodemapping import VMCodeMapping
        from boa3.neo.vm.type.AbiType import AbiType
        from boa3.model.type.itype import IType
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
                                        if isinstance(imported, Import) and imported.origin is not None]
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
        from boa3.model.type.itype import IType
        from boa3.neo.vm.type.AbiType import AbiType

        static_variables = []

        for name, var in self._static_variables.items():
            var_unique_name = self._get_static_var_unique_name(name)
            var_type = var.type.abi_type if isinstance(var.type, IType) else AbiType.Any

            values = [var_unique_name, var_type.name]

            var_slot_index = self._get_static_var_slot_index(name)
            if isinstance(var_slot_index, int):
                values.append(str(var_slot_index))

            static_variables.append(
                ','.join(values)
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
        else:
            variable_original_id = variable_id

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

        from boa3.model.builtin.builtincallable import IBuiltinCallable

        # must map all imports, including inner imports
        index = 0
        while index < len(imported_symbols):
            module_origin, imported = list(imported_symbols.items())[index]
            for name, imported in imported.all_symbols.items():
                if isinstance(imported, Import) and imported.origin not in imported_symbols:
                    imported_symbols[imported.origin] = imported
            index += 1

        # map the modules that have user modules not imported by the entry file
        imported_to_map: Dict[str, Import] = {}
        for name in imported_symbols:
            if any(((not importing_methods  # is importing variables or is a method but not builtin
                     or (isinstance(symbol, Method) and not isinstance(symbol, IBuiltinCallable)))
                    and symbol not in inner_imported_symbols)
                   for name, symbol in imported_symbols[name].all_symbols.items()):
                filtered_name = name.replace('.py', '').replace('/__init__', '')
                imported_to_map[filtered_name] = imported_symbols[name]

        # change the full path names to unique small names
        imports_paths = list(imported_to_map)
        imports_paths.append(self._entry_file_full_path.replace('.py', '').replace('/__init__', ''))

        imports_unique_ids = []
        imports_duplicated_ids = []

        for index in range(len(imports_paths)):
            name = imports_paths[index]
            split_name = name.split('/')
            index = -1
            short_name = split_name[index]
            while short_name in imports_duplicated_ids:
                index -= 1
                short_name = '.'.join(split_name[index:])

            if short_name in imports_unique_ids:
                index_of_duplicated = imports_unique_ids.index(short_name)

                dup_split_name = imports_paths[index_of_duplicated].split('/')
                dup_new_id = short_name
                dup_index = -len(imports_unique_ids[index].split('.'))

                while dup_new_id == short_name:
                    imports_duplicated_ids.append(short_name)
                    index -= 1
                    dup_index -= 1
                    short_name = '.'.join(split_name[index:])
                    dup_new_id = '.'.join(dup_split_name[dup_index:])

                imports_unique_ids[index_of_duplicated] = dup_new_id

            imports_unique_ids.append(short_name)

        return imported_to_map, imports_unique_ids
