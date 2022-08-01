import re
from typing import Dict, List

from boa3.analyser import supportedstandard
from boa3.analyser.astanalyser import IAstAnalyser
from boa3.exception import CompilerError
from boa3.model.event import Event
from boa3.model.imports import importsymbol
from boa3.model.method import Method
from boa3.model.symbol import ISymbol


class StandardAnalyser(IAstAnalyser):
    """
    This class is responsible for the checking if the given contract standards are implemented

    :ivar symbols: a dictionary that maps the global symbols.
    """

    def __init__(self, analyser, symbol_table: Dict[str, ISymbol], log: bool = False):
        from boa3.builtin import NeoMetadata

        super().__init__(analyser.ast_tree, analyser.filename, log=log)

        self.symbols: Dict[str, ISymbol] = symbol_table

        if isinstance(analyser.metadata, NeoMetadata):
            # filter only strings
            analyser.metadata.supported_standards = [standard for standard in analyser.metadata.supported_standards
                                                     if isinstance(standard, str)]
            standards = analyser.metadata.supported_standards
        else:
            standards = []

        self.standards: List[str] = standards
        self._filter_standards_names()
        self._validate_standards()
        self._check_other_implemented_standards()

    def _filter_standards_names(self):
        """
        Converts all the Neo standards names to upper kebab case
        """
        filtered_standards = set()
        for standard in self.standards:
            standard = standard.strip()
            if standard.upper().startswith('NEP'):
                rebab_case = re.sub(r'([A-Z]+|(.\d+)+|\d+)[^a-zA-Z\d]?', r'\g<1>-', standard.upper())
                if rebab_case.endswith('-'):
                    rebab_case = rebab_case[:-1]
                standard = rebab_case

            filtered_standards.add(standard)

        self.standards.clear()
        self.standards.extend(filtered_standards)

    def get_methods_by_display_name(self, method_id: str) -> List[Method]:
        methods = []
        for symbol_id, symbol in self.symbols.items():
            if isinstance(symbol, Method) and symbol.is_public:
                display_name = symbol.external_name if symbol.external_name is not None else symbol_id
                if display_name == method_id:
                    methods.append(symbol)
        return methods

    def _validate_standards(self):
        for standard in self.standards:
            if standard in supportedstandard.neo_standards:
                current_standard = supportedstandard.neo_standards[standard]

                # validate standard's methods
                for standard_method in current_standard.methods:
                    method_id = standard_method.external_name
                    is_implemented = False

                    found_methods = self.get_methods_by_display_name(method_id)
                    for method in found_methods:
                        if isinstance(method, Method) and current_standard.match_definition(standard_method, method):
                            is_implemented = True
                            break

                    if not is_implemented:
                        self._log_error(
                            CompilerError.MissingStandardDefinition(standard, method_id, standard_method)
                        )

                # validate standard's events
                events = [symbol for symbol in self.symbols.values() if isinstance(symbol, Event)]
                # imported events should be included in the validation
                for imported in self._get_all_imports():
                    events.extend([event for event in imported.all_symbols.values() if isinstance(event, Event)])

                for standard_event in current_standard.events:
                    is_implemented = False
                    for event in events:
                        if (event.name == standard_event.name
                                and current_standard.match_definition(standard_event, event)):
                            is_implemented = True
                            break

                    if not is_implemented:
                        self._log_error(
                            CompilerError.MissingStandardDefinition(standard,
                                                                    standard_event.name,
                                                                    standard_event)
                        )

                # validate optional methods
                for optional_method in current_standard.optionals:
                    method_id = optional_method.external_name
                    is_implemented = False

                    found_methods = self.get_methods_by_display_name(method_id)
                    for method in found_methods:
                        if isinstance(method, Method) and current_standard.match_definition(optional_method, method):
                            is_implemented = True
                            break

                    if found_methods and not is_implemented:
                        self._log_error(
                            CompilerError.MissingStandardDefinition(standard, method_id, optional_method)
                        )

    def _get_all_imports(self) -> List[importsymbol.Import]:
        all_imports = [imported for imported in self.symbols.values()
                       if (isinstance(imported, importsymbol.Import)
                           and not isinstance(imported, importsymbol.BuiltinImport))]
        index = 0
        while index < len(all_imports):
            imported = all_imports[index]
            for inner in imported.all_symbols.values():
                if (isinstance(inner, importsymbol.Import)
                        and not isinstance(inner, importsymbol.BuiltinImport)
                        and inner not in all_imports):
                    all_imports.append(inner)
            index += 1

        return all_imports

    def _check_other_implemented_standards(self):
        other_standards = supportedstandard.neo_standards.copy()
        # verify only standards that were not mentioned
        for standard in self.standards:
            if standard in supportedstandard.neo_standards:
                other_standards.pop(standard)

        # gets a list of all events
        events = [symbol for symbol in self.symbols.copy().values() if isinstance(symbol, Event)]
        for imported in self._get_all_imports():
            events.extend([event for event in imported.all_symbols.values() if isinstance(event, Event)])

        # verify if the methods and events that were implemented corresponds to a standard
        for standard in other_standards:

            # verify the methods
            methods_implemented = True
            standard_methods = other_standards[standard].methods
            index = 0

            while methods_implemented and index < len(standard_methods):
                standard_method = standard_methods[index]
                method_id = standard_method.external_name
                found_methods = self.get_methods_by_display_name(method_id)

                methods_implemented = any(
                    other_standards[standard].match_definition(standard_method, method) for method in found_methods
                )
                index += 1

            if not methods_implemented:
                continue    # if even one of the methods was not implemented, then check the next standard

            # verify the events
            events_implemented = True
            standard_events = other_standards[standard].events
            index = 0

            while events_implemented and index < len(standard_events):
                standard_event = standard_events[index]
                events_implemented = any(
                    (event.name == standard_event.name and
                     other_standards[standard].match_definition(standard_event, event)) for event in events
                )
                index += 1

            if not events_implemented:
                continue    # if even one of the events was not implemented, then check the next standard

            self.standards.append(standard)
