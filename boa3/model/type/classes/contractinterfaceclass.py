from typing import List

from boa3.model.callable import Callable
from boa3.model.type.classes.classtype import ClassType
from boa3.model.type.classes.userclass import UserClass
from boa3.neo3.core.types import UInt160


class ContractInterfaceClass(UserClass):
    def __init__(self, identifier: str, contract_hash: UInt160, decorators: List[Callable] = None,
                 bases: List[ClassType] = None):
        from boa3.model.builtin.builtin import Builtin, ContractDecorator

        if not isinstance(decorators, list):
            decorators = [Builtin.ContractInterface]
        elif not any(isinstance(decorator, ContractDecorator) for decorator in decorators):
            decorators.append(Builtin.ContractInterface)

        super().__init__(identifier, decorators, bases)
        self.contract_hash = contract_hash

    @property
    def is_interface(self) -> bool:
        return True
