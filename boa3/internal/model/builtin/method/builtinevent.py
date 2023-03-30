import ast
from abc import ABC
from typing import Dict, List, Optional, Tuple

from boa3.internal.model.builtin.builtincallable import IBuiltinCallable
from boa3.internal.model.event import Event
from boa3.internal.model.variable import Variable


class IBuiltinEvent(IBuiltinCallable, Event, ABC):
    def __init__(self, identifier: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None,
                 vararg: Optional[Tuple[str, Variable]] = None,
                 kwargs: Optional[Dict[str, Variable]] = None):
        from boa3.internal.model.type.type import Type
        super().__init__(identifier, args, vararg, kwargs, defaults, Type.none)

        # constructor of IBuiltinCallable and Event classes are conflicting
        self._identifier = identifier
        self.name = identifier
        self.args = args if args is not None else {}
        self.defaults = defaults if defaults is not None else []
