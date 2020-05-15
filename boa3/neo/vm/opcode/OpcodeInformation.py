from boa3.neo.vm.opcode.Opcode import Opcode


class OpcodeInformation:
    """
    Stores the information about a specific :class:`Opcode`

    :ivar opcode: the opcode of the code
    :ivar data_len: the size in bytes of the expected operand. Zero by default.
    :ivar max_data_len: the max size in bytes of the operand. Same value as data_len if size is constant.
    """
    def __init__(self, opcode: Opcode, min_data_len: int = 0, max_data_len: int = 0):
        self.opcode: Opcode = opcode

        if min_data_len < 0:
            min_data_len = 0
        self.data_len: int = min_data_len

        if max_data_len < min_data_len:
            max_data_len = min_data_len
        self.max_data_len: int = max_data_len
