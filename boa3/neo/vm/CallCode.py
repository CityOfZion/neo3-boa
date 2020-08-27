from boa3.model.callable import Callable
from boa3.neo.vm.VMCode import VMCode


class CallCode(VMCode):
    """
    Represents a Neo VM function call code

    :ivar info: the opcode information of the code
    :ivar data: the data in bytes of the code. Empty byte array by default.
    """

    def __init__(self, target_callable: Callable):
        """
        :param target_callable: the calling method
        :type target_callable: Method
        """
        self._target_callable: Callable = target_callable
        from boa3.neo.vm.opcode.OpcodeInfo import OpcodeInfo
        super().__init__(OpcodeInfo.CALL)

    @property
    def target(self) -> VMCode:
        return self._target_callable.init_bytecode
