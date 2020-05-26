import sys

from boa3.constants import SIZE_OF_INT32
from boa3.neo.vm.type.Integer import Integer


class Serializer:
    """
    This class is responsible for serialize Python primitive types into bytes
    """

    def __init__(self):
        self.__result = bytearray()

    @property
    def result(self) -> bytearray:
        """
        Gets the serializer written data

        :return: the written data as a bytearray
        :rtype: bytearray
        """
        return self.__result

    def write_bytes(self, value: bytes, size: int = 0):
        """
        Write the given bytes object into the serializer output

        :param value: bytes to be written
        :param size: the number of bytes that must filled
        """
        # if the number of bytes is greater than the specified size, the remaining will be ignored
        if 0 < size < len(value):
            value = value[0:size]

        self.__result.extend(value)
        # if the number of bytes is greater than the specified, fill the remaining with an empty bytearray
        if size > len(value):
            self.__fill_with_empty(size - len(value))

    def write_byte_array(self, value: bytearray, size: int = 0):
        """
        Write the given bytearray object into the serializer output

        :param value: bytes to be written
        :param size: the number of bytes that must filled
        """
        # if the number of bytes is greater than the specified size, the remaining will be ignored
        if 0 < size < len(value):
            value = value[0:size]

        self.__result.extend(value)
        # if the number of bytes is greater than the specified, fill the remaining with an empty bytearray
        if size > len(value):
            self.__fill_with_empty(size - len(value))

    def write_string(self, string: str, size: int):
        """
        Write the given string into the serializer output

        :param string: string to be written
        :param size: the number of bytes that the string must fill
        """
        # if the size of the string is greater than the specified size, the remaining will be ignored
        if len(string) > size:
            string = string[0:size]

        str_bytes = bytearray(string, encoding='UTF-8')
        self.__result.extend(str_bytes)

        # if the size of the string is less than the specified, fill the remaining with an empty bytearray
        if len(string) < size:
            self.__fill_with_empty(size - len(string))

    def write_integer(self, integer: int, size: int = SIZE_OF_INT32):
        """
        Write the given integer value into the serializer output

        :param integer: integer value to be written
        :param size: the number of bytes that the string must fill
        """
        int_bytes = integer.to_bytes(size, sys.byteorder)
        self.__result.extend(int_bytes)

    def write_value(self, var_bytes: bytes):
        """
        Write the given bytes object and size into the serializer output

        :param var_bytes: bytes to be written
        """
        value_bytes = bytearray()
        value_bytes.extend(Integer(len(var_bytes)).to_byte_array())
        value_bytes.extend(var_bytes)
        self.__result.extend(value_bytes)

    def __fill_with_empty(self, length: int):
        """
        Write an empty array with the given length into the serializer output

        :param length: the number of bytes that must be filled
        """
        self.__result.extend(bytes(length))
