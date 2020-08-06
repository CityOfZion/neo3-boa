import ast
from typing import Dict, List, Optional

from boa3.model.callable import Callable
from boa3.model.type.type import Type
from boa3.model.variable import Variable


class Event(Callable):
    def __init__(self, args: Dict[str, Variable] = None, defaults: List[ast.AST] = None,
                 is_public: bool = False, origin_node: Optional[ast.AST] = None):
        super().__init__(args, defaults, Type.none, is_public, origin_node)

    @property
    def shadowing_name(self) -> str:
        return 'event'
