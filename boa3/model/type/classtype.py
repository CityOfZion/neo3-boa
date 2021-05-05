from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.symbol import ISymbol
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.StackItem import StackItemType


class ClassType(IType, ABC):
    """
    An abstract class used to represent Python class
    """

    def __init__(self, identifier: str):
        super().__init__(identifier)

    @property
    @abstractmethod
    def variables(self) -> Dict[str, Variable]:
        return {}

    @property
    @abstractmethod
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    @abstractmethod
    def class_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        # TODO: Change to return only class symbols or instance symbols
        s = {}
        s.update(self.class_methods)
        s.update(self.variables)
        s.update(self.properties)
        s.update(self.instance_methods)
        return s

    @property
    @abstractmethod
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    @abstractmethod
    def constructor_method(self) -> Optional[Method]:
        """
        If the class constructor is None, it mustn't allow instantiation of this class
        """
        pass

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.Array

    def is_instance_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        # TODO: Implement when the validation of created types is fixed
        return []
