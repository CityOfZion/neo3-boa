from typing import Optional

from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.opcode.OpcodeInformation import OpcodeInformation


class VMCode:
    """
    Represents a Neo VM code

    :ivar opcode: the opcode of the code
    :ivar data: the data in bytes of the code. Empty byte array by default.
    """

    def __init__(self, op_info: OpcodeInformation, last_code=None, data: bytes = bytes()):
        """
        :param op_info: information of the opcode of the code
        :param last_code: the previous code in the bytecode. None if it's the first.
        :type last_code: VMCode or None
        :param data: the data in bytes of the code. Empty byte array by default.
        """
        self._last_code = last_code    # type:Optional[VMCode]
        self.info: OpcodeInformation = op_info
        self.data: bytes = self.__format_data(data)

    @property
    def start_address(self) -> int:
        """
        Gets the start address of this code

        :return: the first address of the code
        """
        if self._last_code is None:
            return 0
        else:
            return self._last_code.end_address + 1

    @property
    def end_address(self) -> int:
        """
        Gets the end address of this code

        :return: the last address of the code
        """
        return self.start_address + len(self.data)

    @property
    def opcode(self) -> Opcode:
        """
        Gets the Neo VM opcode of the code

        :return: the opcode of the code
        """
        return self.info.opcode

    def update(self, opcode: OpcodeInformation, data: bytes = bytes()):
        self.info = opcode
        self.data = self.__format_data(data)

    def __format_data(self, data: bytes) -> bytes:
        data_len: int = len(data)
        min_data_len: int = self.info.data_len
        max_data_len: int = self.info.max_data_len

        if data_len < min_data_len:
            data = bytes(bytearray(data).zfill(min_data_len))
        elif data_len > max_data_len:
            data = data_len[0:max_data_len]

        return data

    def __str__(self) -> str:
        return self.opcode.name + ' ' + self.data.hex()
