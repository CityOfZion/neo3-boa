import re
from typing import Dict, List

from boa3.analyser import supportedstandard
from boa3.analyser.astanalyser import IAstAnalyser
from boa3.exception import CompilerError
from boa3.model.event import Event
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

    def _filter_standards_names(self):
        """
        Converts all the standards names to upper kebab case
        """
        filtered_standards = set()
        for standard in self.standards:
            rebab_case = re.sub(r'([a-z]+|[A-Z]+[a-z]*|\d+)[^a-zA-Z\d]?', r'\g<1>-', standard)
            if rebab_case.endswith('-'):
                rebab_case = rebab_case[:-1]
            rebab_case = rebab_case.upper()
            filtered_standards.add(rebab_case)

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

                # validade standard's methods
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

                # validade standard's events
                events = [symbol for symbol in self.symbols.values() if isinstance(symbol, Event)]
                for standard_event in current_standard.events:
                    is_implemented = False
                    for event in events:
                        if event.name == standard_event.name and current_standard.match_definition(standard_event, event):
                            is_implemented = True
                            break

                    if not is_implemented:
                        self._log_error(
                            CompilerError.MissingStandardDefinition(standard,
                                                                    standard_event.name,
                                                                    standard_event)
                        )

    def _check_other_implemented_standards(self):
        # TODO: Implement when detecting standards from implemented methods and events
        pass
