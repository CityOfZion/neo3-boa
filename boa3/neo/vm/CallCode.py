from typing import Optional

from boa3.model.method import Method
from boa3.neo.vm.VMCode import VMCode
from boa3.neo.vm.opcode.OpcodeInformation import OpcodeInformation
from boa3.neo.vm.type.Integer import Integer


class CallCode(VMCode):
    """
    Represents a Neo VM function call code

    :ivar info: the opcode information of the code
    :ivar data: the data in bytes of the code. Empty byte array by default.
    """
    from boa3.neo.vm.opcode.OpcodeInfo import OpcodeInfo
    _CALL = OpcodeInfo.CALL
    _CALL_L = OpcodeInfo.CALL_L

    def __init__(self, target_method: Method, last_code: Optional[VMCode] = None):
        """
        :param op_info: information of the opcode of the code
        :param last_code: the previous code in the bytecode. None if it's the first.
        :type last_code: VMCode or None
        :param target_method: the calling method
        :type target_method: Method
        """
        self._target_method: Method = target_method
        super().__init__(self._CALL, last_code)

    @property
    def info(self) -> OpcodeInformation:
        if len(self._unformatted_data.to_byte_array(signed=True)) > self._CALL.data_len:
            return self._CALL_L
        return self._CALL

    @property
    def data(self) -> bytes:
        value = self._unformatted_data
        self._data = value.to_byte_array(signed=True, min_length=self.info.data_len)[:self.info.max_data_len]
        return super().data

    @property
    def _unformatted_data(self) -> Integer:
        target = self._target_method.start_address
        return Integer((target if target is not None else self.start_address) - self.start_address)
