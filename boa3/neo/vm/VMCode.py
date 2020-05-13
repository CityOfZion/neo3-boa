from typing import Optional

from boa3.neo.vm.Opcode import Opcode


class VMCode:
    """
    Represents a Neo VM code

    :ivar opcode: the opcode of the code
    :ivar data: the data in bytes of the code. Empty byte array by default.
    """
    def __init__(self, opcode: Opcode, last_code=None, data: bytes = None):
        """
        :param opcode: the opcode of the code
        :param last_code: the previous code in the bytecode. None if it's the first.
        :type last_code: VMCode or None
        :param data: the data in bytes of the code. Empty byte array by default.
        """
        self.opcode: Opcode = opcode
        self.__last_code = last_code    # type:Optional[VMCode]
        if data is None:
            data = bytes()
        self.data: bytes = data

    @property
    def start_address(self) -> int:
        """
        Gets the start address of this code

        :return: the first address of the code
        """
        if self.__last_code is None:
            return 0
        else:
            return self.__last_code.end_address + 1

    @property
    def end_address(self) -> int:
        """
        Gets the end address of this code

        :return: the last address of the code
        """
        return self.start_address + len(self.data)
