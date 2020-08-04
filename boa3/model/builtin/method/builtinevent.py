from abc import ABC
from typing import Dict

from boa3.model.builtin.builtincallable import IBuiltinCallable
from boa3.model.event import Event
from boa3.model.variable import Variable


class IBuiltinEvent(IBuiltinCallable, Event, ABC):
    def __init__(self, identifier: str, args: Dict[str, Variable] = None):
        from boa3.model.type.type import Type
        super().__init__(identifier, args, Type.none)
