import ast
from typing import Dict, List, Optional, Tuple

from boa3.model.callable import Callable
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.type.type import Type
from boa3.model.variable import Variable


class Event(Callable, IdentifiedSymbol):
    def __init__(self, event_id: str, args: Dict[str, Variable] = None,
                 vararg: Optional[Tuple[str, Variable]] = None,
                 kwargs: Optional[Dict[str, Variable]] = None,
                 defaults: List[ast.AST] = None,
                 origin_node: Optional[ast.AST] = None):
        super().__init__(args, vararg, kwargs, defaults, Type.none, True, origin_node)

        self.name: str = event_id
        self._identifier: str = self.name

    @property
    def shadowing_name(self) -> str:
        return 'event'

    @property
    def identifier(self) -> str:
        return self.name

    @property
    def args_to_generate(self) -> Dict[str, Variable]:
        return self.args.copy()

    @property
    def generate_name(self) -> bool:
        return True
