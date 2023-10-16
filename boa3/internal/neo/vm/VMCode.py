from __future__ import annotations

from typing import Optional

from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.opcode.OpcodeInformation import OpcodeInformation
from boa3.internal.neo.vm.type.Integer import Integer


class VMCode:
    """
    Represents a Neo VM code

    :ivar info: the opcode information of the code
    :ivar data: the data in bytes of the code. Empty byte array by default.
    """

    def __init__(self, op_info: OpcodeInformation, data: bytes = None):
        """
        :param op_info: information of the opcode of the code
        :param data: the data in bytes of the code. Empty byte array by default.
        """
        if data is None:
            data = bytes(op_info.data_len)
        self._info: OpcodeInformation = op_info
        self._target: Optional[VMCode] = None
        self._data: bytes = data

    @property
    def info(self) -> OpcodeInformation:
        """
        Gets the Neo VM opcode information

        :return: the opcode of the code.
        """
        return self._info

    @property
    def data(self) -> bytes:
        """
        Gets the Neo VM data of the code

        :return: the formatted data in bytes of the code.
        """
        data: bytearray = bytearray(self.raw_data)
        info = self.info

        if len(data) < info.data_len:
            data.extend(bytes(info.data_len))
        elif len(data) > info.max_data_len:
            data = data[:info.max_data_len]
        return data

    @property
    def raw_data(self) -> bytes:
        """
        Gets the Neo VM raw data of the code

        :return: the unformatted data in bytes of the code.
        """
        if self.target is None:
            return self._data
        else:
            from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
            code_mapping = VMCodeMapping.instance()
            self_start = code_mapping.get_start_address(self)
            target_start = code_mapping.get_start_address(self.target)

            if self_start == target_start:
                return self._data

            return (Integer(target_start - self_start)
                    .to_byte_array(signed=True, min_length=self._info.data_len))

    @property
    def size(self) -> int:
        return len(self._info.opcode) + len(self.data)

    @property
    def opcode(self) -> Opcode:
        """
        Gets the Neo VM opcode of the code

        :return: the opcode of the code
        """
        return self.info.opcode

    @property
    def target(self) -> VMCode:
        """
        Gets the target code of this code

        :return: the target code if this is a control code. None otherwise
        :rtype: VMCode
        """
        return self._target if OpcodeHelper.has_target(self.opcode) else None

    def set_target(self, target_code):
        """
        Set the target code if this instruction's opcode requires a target

        :param target_code: the target code of this instruction
        :type target_code: VMCode
        """
        if OpcodeHelper.has_target(self.opcode):
            self._target = target_code

    def set_opcode(self, opcode):
        if (isinstance(opcode, OpcodeInformation) and
                OpcodeHelper.has_target(opcode.opcode) == OpcodeHelper.has_target(self.opcode)):
            self._info = opcode

    def __str__(self) -> str:
        return self.opcode.name + ' ' + self.data.hex()
