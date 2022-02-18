import abc
from typing import List, Union

from boa3.model.event import Event
from boa3.model.method import Method


class INeoStandard(abc.ABC):
    def __init__(self, methods: List[Method], events: List[Event]):
        self.methods: List[Method] = methods.copy()
        self.events: List[Event] = events.copy()

    def match_definition(self, standard: Union[Method, Event], symbol: Union[Method, Event]) -> bool:
        if not isinstance(standard, (Method, Event)) or not isinstance(symbol, (Method, Event)):
            return False

        standard_symbols = self.methods if isinstance(symbol, Method) else self.events
        if standard not in standard_symbols:
            return False

        return self._have_same_signature(standard, symbol)

    def _have_same_signature(self, symbol: Union[Method, Event], other: Union[Method, Event]) -> bool:
        if (isinstance(symbol, Method) and not isinstance(other, Method)
                or isinstance(symbol, Event) and not isinstance(other, Event)):
            return False

        if symbol.return_type != other.return_type:
            return False

        if symbol.is_public != other.is_public:
            return False

        if symbol.is_safe != other.is_safe:
            return False

        if len(symbol.args) != len(other.args):
            return False

        method_args = list(symbol.args.values())
        other_args = list(other.args.values())
        for index in range(len(method_args)):
            if method_args[index].type != other_args[index].type:
                return False

        return True
