import abc
from typing import Dict, List, Union

from boa3.model.event import Event
from boa3.model.method import Method


class INeoStandard(abc.ABC):
    def __init__(self, methods: Dict[str, Method], events: List[Event]):
        self.methods: Dict[str, Method] = methods
        self.events: Dict[str, Event] = {event.name: event for event in events}

    def match_definition(self, symbol_id: str, symbol: Union[Method, Event]) -> bool:
        if not isinstance(symbol, (Method, Event)) or not isinstance(symbol_id, str):
            return False

        standard_symbols = self.methods if isinstance(symbol, Method) else self.events
        if symbol_id not in standard_symbols:
            return False

        standard_def = standard_symbols[symbol_id]
        return self._have_same_signature(standard_def, symbol)

    def _have_same_signature(self, symbol: Union[Method, Event], other: Union[Method, Event]) -> bool:
        if (isinstance(symbol, Method) and not isinstance(other, Method)
                or isinstance(symbol, Event) and not isinstance(other, Event)):
            return False

        if symbol.return_type != other.return_type:
            return False

        if symbol.is_public != other.is_public:
            return False

        if len(symbol.args) != len(other.args):
            return False

        method_args = list(symbol.args.values())
        other_args = list(other.args.values())
        for index in range(len(method_args)):
            if method_args[index].type != other_args[index].type:
                return False

        return True
