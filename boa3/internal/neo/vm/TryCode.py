from boa3.internal.neo.vm.VMCode import VMCode
from boa3.internal.neo.vm.type.Integer import Integer


class TryCode(VMCode):
    """
    Represents a Neo VM function try code

    :ivar info: the opcode information of the code
    :ivar data: the data in bytes of the code. Empty byte array by default.
    """

    def __init__(self, except_start_code: VMCode | None = None, finally_start_code: VMCode | None = None):
        """
        :param except_start_code: the first code of the except body
        :type except_start_code: VMCode or None
        """
        self._except_start_code: VMCode | None = except_start_code
        self._finally_start_code: VMCode | None = finally_start_code
        from boa3.internal.neo.vm.opcode.OpcodeInfo import OpcodeInfo
        super().__init__(OpcodeInfo.TRY)

    @property
    def target(self) -> VMCode:
        return self._except_start_code if self._finally_start_code is None else self._finally_start_code

    def set_except_code(self, except_code: VMCode):
        if self._except_start_code is None and except_code is not None:
            self._except_start_code = except_code

    def set_finally_code(self, finally_code: VMCode):
        if self._finally_start_code is None and finally_code is not None:
            self._finally_start_code = finally_code

    @property
    def data(self) -> bytes:
        """
        Gets the Neo VM data of the code

        :return: the formatted data in bytes of the code.
        """
        catch_data: bytes = self._get_raw_data(self._except_start_code)
        finally_data: bytes = self._get_raw_data(self._finally_start_code)

        min_data_len = self._info.data_len // 2
        max_data_len = self._info.max_data_len // 2

        return (self._format_data(catch_data, min_data_len, max_data_len)
                + self._format_data(finally_data, min_data_len, max_data_len))

    def _format_data(self, data: bytes, min_data_len: int, max_data_len: int = -1) -> bytes:
        if max_data_len < min_data_len:
            max_data_len = min_data_len
        mutable_data = bytearray(data)

        if len(mutable_data) < min_data_len:
            mutable_data.extend(bytes(min_data_len))
        elif len(mutable_data) > max_data_len:
            mutable_data = mutable_data[:max_data_len]
        return bytes(mutable_data)

    def _get_raw_data(self, opcode: VMCode) -> bytes:
        """
        Gets the Neo VM raw data of the code

        :return: the unformatted data in bytes of the code.
        """
        min_len = self._info.data_len // 2  # for try opcode, data_len adds catch and finally addresses
        if opcode is None:
            return bytes(min_len)
        else:
            from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
            code_mapping = VMCodeMapping.instance()
            self_start = code_mapping.get_start_address(self)
            target_start = code_mapping.get_start_address(opcode)

            return (Integer(target_start - self_start)
                    .to_byte_array(signed=True, min_length=min_len))

    @property
    def raw_data(self) -> bytes:
        catch_data: bytes = self._get_raw_data(self._except_start_code)
        finally_data: bytes = self._get_raw_data(self._finally_start_code)

        size = max(len(catch_data), len(finally_data))

        return self._format_data(catch_data, size) + self._format_data(finally_data, size)
