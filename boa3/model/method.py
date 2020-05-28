from typing import Dict, Optional

from boa3.model.expression import IExpression
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class Method(IExpression):
    """
    A class used to represent a function or a class method

    :ivar args: a dictionary that maps each arg with its name. Empty by default.
    :ivar locals: a dictionary that maps each local variable with its name. Empty by default.
    :ivar is_public: a boolean value that specifies if the method is public. False by default.
    :ivar return_type: the return type of the method. None by default.
    """

    def __init__(self, args: Dict[str, Variable] = None, return_type: IType = None, is_public: bool = False):
        from boa3.neo.vm.VMCode import VMCode
        if args is None:
            args = {}
        self.args: Dict[str, Variable] = args
        self.return_type: IType = return_type

        self.is_public: bool = is_public
        self.is_main_method: bool = False

        self.locals: Dict[str, Variable] = {}
        self.init_bytecode: Optional[VMCode] = None

    @property
    def shadowing_name(self) -> str:
        return 'method'

    def include_variable(self, var_id: str, var: Variable):
        """
        Includes a variable into the list of locals

        :param var_id: variable identifier
        :param var: variable to be included
        """
        if var_id not in self.symbols:
            self.locals[var_id] = var

    @property
    def type(self) -> IType:
        return self.return_type

    @property
    def symbols(self) -> Dict[str, Variable]:
        """
        Gets all the symbols in the module

        :return: a dictionary that maps each symbol in the module with its name
        """
        symbols = {}
        symbols.update(self.args)
        symbols.update(self.locals)
        return symbols

    @property
    def bytecode_address(self) -> Optional[int]:
        """
        Gets the address where this method starts in the bytecode

        :return: the first address of the method
        """
        if self.init_bytecode is None:
            return None
        else:
            return self.init_bytecode.start_address

    def set_as_main_method(self):
        self.is_main_method = True
        self.is_public = True
