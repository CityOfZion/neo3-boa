import re

from boa3.internal.analyser import supportedstandard
from boa3.internal.analyser.astanalyser import IAstAnalyser
from boa3.internal.exception import CompilerError
from boa3.internal.model.event import Event
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol


class StandardAnalyser(IAstAnalyser):
    """
    This class is responsible for the checking if the given contract standards are implemented

    :ivar symbols: a dictionary that maps the global symbols.
    """

    def __init__(self, analyser, symbol_table: dict[str, ISymbol],
                 log: bool = False, fail_fast: bool = True):
        from boa3.builtin.compile_time import NeoMetadata

        super().__init__(analyser.ast_tree, analyser.filename, analyser.root, log=log, fail_fast=fail_fast)

        self.symbols: dict[str, ISymbol] = symbol_table

        if isinstance(analyser.metadata, NeoMetadata):
            # filter only strings
            analyser.metadata.supported_standards = [standard for standard in analyser.metadata.supported_standards
                                                     if isinstance(standard, str)]
            standards = analyser.metadata.supported_standards
        else:
            standards = []

        self.standards: list[str] = standards
        self._analyser = analyser
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

    def get_methods_by_display_name(self, method_id: str) -> list[Method]:
        methods = []
        for symbol_id, symbol in self.symbols.items():
            if isinstance(symbol, Method) and symbol.is_public:
                display_name = symbol.external_name if symbol.external_name is not None else symbol_id
                if display_name == method_id:
                    methods.append(symbol)
        return methods

    def _validate_standards(self):
        try:
            for standard in self.standards:
                if standard in supportedstandard.neo_standards:
                    standard_was_found = False
                    standard_errors = {}

                    standard_index = 0
                    while standard_index < len(supportedstandard.neo_standards[standard]) and not standard_was_found:
                        current_standard = supportedstandard.neo_standards[standard][standard_index]
                        current_standard_errors = []

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
                                current_standard_errors.append(
                                    CompilerError.MissingStandardDefinition(standard, method_id, standard_method)
                                )

                        # validate standard's events
                        events = [symbol for symbol in self.symbols.values() if isinstance(symbol, Event)]
                        # imported events should be included in the validation
                        for import_ in self._analyser.get_imports():
                            events.extend([event for event in import_.symbol_table.values()
                                           if isinstance(event, Event) and event not in events])

                        for standard_event in current_standard.events:
                            is_implemented = False
                            for event in events:
                                if (event.name == standard_event.name
                                        and current_standard.match_definition(standard_event, event)):
                                    is_implemented = True
                                    break

                            if not is_implemented:
                                current_standard_errors.append(
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
                                current_standard_errors.append(
                                    CompilerError.MissingStandardDefinition(standard, method_id, optional_method)
                                )

                        standard_errors[standard_index] = current_standard_errors
                        standard_was_found = len(current_standard_errors) == 0
                        standard_index += 1

                    if not standard_was_found:
                        for error in standard_errors[0]:
                            self._log_error(error)

        except CompilerError.CompilerError:
            # stops the analyser if fail fast is activated
            pass

    def _check_other_implemented_standards(self):
        other_standards = supportedstandard.neo_standards.copy()
        # verify only standards that were not mentioned
        for standard in self.standards:
            if standard in supportedstandard.neo_standards:
                other_standards.pop(standard)

        # gets a list of all events
        events = [symbol for symbol in self.symbols.copy().values() if isinstance(symbol, Event)]
        for import_ in self._analyser.get_imports():
            events.extend([event for event in import_.symbol_table.values() if isinstance(event, Event)])

        # verify if the methods and events that were implemented corresponds to a standard
        for standard in other_standards:
            for current_standard in other_standards[standard]:
                # verify the methods
                methods_implemented = True
                standard_methods = current_standard.methods
                index = 0

                while methods_implemented and index < len(standard_methods):
                    standard_method = standard_methods[index]
                    method_id = standard_method.external_name
                    found_methods = self.get_methods_by_display_name(method_id)

                    methods_implemented = any(
                        current_standard.match_definition(standard_method, method) for method in found_methods
                    )
                    index += 1

                if not methods_implemented:
                    continue    # if even one of the methods was not implemented, then check the next standard

                # verify the events
                events_implemented = True
                standard_events = current_standard.events
                index = 0

                while events_implemented and index < len(standard_events):
                    standard_event = standard_events[index]
                    events_implemented = any(
                        (event.name == standard_event.name and
                         current_standard.match_definition(standard_event, event)) for event in events
                    )
                    index += 1

                if not events_implemented:
                    continue    # if even one of the events was not implemented, then check the next standard

                self.standards.append(standard)
                break
