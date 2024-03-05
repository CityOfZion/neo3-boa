import abc

from boa3.internal.model.event import Event
from boa3.internal.model.method import Method


class INeoStandard(abc.ABC):
    def __init__(self, methods: list[Method], events: list[Event], optionals: list[Method] | None = None):
        if optionals is None:
            optionals = []
        self.methods: list[Method] = methods.copy()
        self.events: list[Event] = events.copy()
        self.optionals: list[Method] = optionals.copy()

    def match_definition(self, standard: Method | Event, symbol: Method | Event) -> bool:
        if not isinstance(standard, (Method, Event)) or not isinstance(symbol, (Method, Event)):
            return False

        standard_symbols = self.methods + self.optionals if isinstance(symbol, Method) else self.events
        if standard not in standard_symbols:
            return False

        return self._have_same_signature(standard, symbol)

    def _have_same_signature(self, symbol: Method | Event, other: Method | Event) -> bool:
        if (isinstance(symbol, Method) and not isinstance(other, Method)
                or isinstance(symbol, Event) and not isinstance(other, Event)):
            return False

        if symbol.return_type != other.return_type and not (
                # verifies if both return types are equal if they are a neo3-boa type
                symbol.return_type.is_type_of(other.return_type) and other.return_type.is_type_of(symbol.return_type)):
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
            if hasattr(symbol, 'literal_implementation') and symbol.literal_implementation:
                if method_args[index].type != other_args[index].type:
                    return False
            else:
                if not method_args[index].type.is_type_of(other_args[index].type):
                    return False
        return True
