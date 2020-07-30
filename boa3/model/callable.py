import ast
from abc import ABC
from typing import Dict, Optional

from boa3.model.expression import IExpression
from boa3.model.type.type import IType, Type
from boa3.model.variable import Variable
from boa3.neo.vm.VMCode import VMCode


class Callable(IExpression, ABC):
    """
    A class used to represent a function or a class method

    :ivar args: a dictionary that maps each arg with its name. Empty by default.
    :ivar is_public: a boolean value that specifies if the method is public. False by default.
    :ivar return_type: the return type of the method. None by default.
    """

    def __init__(self, args: Dict[str, Variable] = None, return_type: IType = Type.none,
                 is_public: bool = False, origin_node: Optional[ast.AST] = None):
        if args is None:
            args = {}
        self.args: Dict[str, Variable] = args
        self.return_type: IType = return_type
        self._origin_node = origin_node
        self.is_public: bool = is_public

        self.init_address: Optional[int] = None
        self.init_bytecode: Optional[VMCode] = None
        self.end_bytecode: Optional[VMCode] = None

    @property
    def type(self) -> IType:
        return self.return_type

    @property
    def symbols(self) -> Dict[str, Variable]:
        """
        Gets all the symbols in the method

        :return: a dictionary that maps each symbol in the module with its name
        """
        return self.args.copy()

    @property
    def origin(self) -> ast.AST:
        """
        Returns the method origin ast node.

        :return: the ast node that describes this method. None if it is not from a ast.
        """
        return self._origin_node

    @property
    def start_address(self) -> Optional[int]:
        """
        Gets the address where this method starts in the bytecode

        :return: the first address of the method
        """
        if self.init_bytecode is None:
            return self.init_address
        else:
            from boa3.compiler.vmcodemapping import VMCodeMapping
            return VMCodeMapping.instance().get_start_address(self.init_bytecode)

    @property
    def end_address(self) -> Optional[int]:
        """
        Gets the address of this method's last operation in the bytecode

        :return: the last address of the method
        """
        if self.end_bytecode is None:
            return self.start_address
        else:
            from boa3.compiler.vmcodemapping import VMCodeMapping
            return VMCodeMapping.instance().get_end_address(self.end_bytecode)
