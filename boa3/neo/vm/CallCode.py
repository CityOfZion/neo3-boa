from typing import Optional

from boa3.model.method import Method
from boa3.neo.vm.VMCode import VMCode


class CallCode(VMCode):
    """
    Represents a Neo VM function call code

    :ivar info: the opcode information of the code
    :ivar data: the data in bytes of the code. Empty byte array by default.
    """

    def __init__(self, target_method: Method):
        """
        :param target_method: the calling method
        :type target_method: Method
        """
        self._target_method: Method = target_method
        from boa3.neo.vm.opcode.OpcodeInfo import OpcodeInfo
        super().__init__(OpcodeInfo.CALL)

    @property
    def target(self) -> VMCode:
        return self._target_method.init_bytecode
