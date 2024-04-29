import ast

from boa3.internal.model.callable import Callable
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class Event(Callable, IdentifiedSymbol):
    def __init__(self,
                 event_id: str, args: dict[str, Variable] = None,
                 vararg: tuple[str, Variable] | None = None,
                 kwargs: dict[str, Variable] | None = None,
                 defaults: list[ast.AST] = None,
                 origin_node: ast.AST | None = None,
                 deprecated: bool = False
                 ):
        super().__init__(args, vararg, kwargs, defaults, Type.none, True, origin_node, deprecated=deprecated)

        self.name: str = event_id
        self._identifier: str = None

    @property
    def shadowing_name(self) -> str:
        return 'event'

    @property
    def identifier(self) -> str:
        if self._identifier is None:
            # internal identifier should not be the name to avoid nonexistent duplicated symbol ids
            self._identifier = f'-{self.name}-{hex(id(self))}'
        return self._identifier

    @property
    def args_to_generate(self) -> dict[str, Variable]:
        return self.args.copy()

    @property
    def generate_name(self) -> bool:
        return True
