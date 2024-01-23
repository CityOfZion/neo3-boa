from boa3.internal.model.callable import Callable
from boa3.internal.model.type.classes.classtype import ClassType
from boa3.internal.model.type.classes.contractinterfacehash import ContractHashProperty
from boa3.internal.model.type.classes.userclass import UserClass
from boa3.internal.neo3.core.types import UInt160


class ContractInterfaceClass(UserClass):
    def __init__(self, identifier: str, contract_hash: UInt160, decorators: list[Callable] = None,
                 bases: list[ClassType] = None):
        from boa3.internal.model.builtin.builtin import Builtin, ContractDecorator

        if not isinstance(decorators, list):
            decorators = [Builtin.ContractInterface]
        elif not any(isinstance(decorator, ContractDecorator) for decorator in decorators):
            decorators.append(Builtin.ContractInterface)

        super().__init__(identifier, decorators, bases)
        self.contract_hash = contract_hash

        contract_hash_property = ContractHashProperty(f'-{identifier}_hash', contract_hash.to_array())
        self.include_property('hash', contract_hash_property)

    @property
    def is_interface(self) -> bool:
        return True
