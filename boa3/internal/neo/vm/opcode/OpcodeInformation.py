from __future__ import annotations

from typing import Optional

from boa3.internal.neo.vm.opcode.Opcode import Opcode


class OpcodeInformation:
    """
    Stores the information about a specific :class:`Opcode`

    :ivar opcode: the opcode of the code
    :ivar data_len: the size in bytes of the expected operand. Zero by default.
    :ivar max_data_len: the max size in bytes of the operand. Same value as data_len if size is constant.
    """

    def __init__(self, opcode: Opcode, min_data_len: int = 0, extra_data_max_len: int = 0, stack_items: int = 0):
        self.opcode: Opcode = opcode

        if min_data_len < 0:
            min_data_len = 0
        self.data_len: int = min_data_len

        if extra_data_max_len < 0:
            extra_data_max_len = 0
        self.max_data_len: int = min_data_len + extra_data_max_len

        if stack_items < 0:
            stack_items = 0
        self.stack_items: int = stack_items

    def get_large(self) -> Optional[OpcodeInformation]:
        large_op = self.opcode.get_large
        if large_op is None:
            return None

        from boa3.internal.neo.vm.opcode.OpcodeInfo import OpcodeInfo
        return OpcodeInfo.get_info(large_op)
