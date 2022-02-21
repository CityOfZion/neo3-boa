from typing import Any

from boa3.builtin.type import ByteString


class StdLib:
    """
    A class used to represent StdLib native contract
    """

    @classmethod
    def serialize(cls, item: Any) -> bytes:
        """
        Serializes the given value into its bytes representation.

        :param item: value to be serialized
        :type item: Any
        :return: the serialized value
        :rtype: bytes

        :raise Exception: raised if the item's type is not serializable.
        """
        pass

    @classmethod
    def deserialize(cls, data: bytes) -> Any:
        """
        Deserializes the given bytes value.

        :param data: serialized value
        :type data: bytes
        :return: the deserialized result
        :rtype: Any

        :raise Exception: raised when the date doesn't represent a serialized value.
        """
        pass

    @classmethod
    def json_serialize(cls, item: Any) -> str:
        """
        Serializes an item into a json.

        :param item: The item that will be serialized
        :type item: Any
        :return: The serialized item
        :rtype: str

        :raise Exception: raised if the item is an integer value out of the Neo's accepted range, is a dictionary with a
            bytearray key, or isn't serializable.
        """
        pass

    @classmethod
    def json_deserialize(cls, json: str) -> Any:
        """
        Deserializes a json into some valid type.

        :param json: A json that will be deserialized
        :type json: str
        :return: The deserialized json
        :rtype: Any

        :raise Exception: raised if jsons deserialization is not valid.
        """
        pass

    @classmethod
    def base64_decode(cls, key: str) -> bytes:
        """
        Decodes a string value encoded with base64.

        :param key: string value to be decoded
        :type key: str
        :return: the decoded string
        :rtype: bytes
        """
        pass

    @classmethod
    def base64_encode(cls, key: bytes) -> str:
        """
        Encodes a bytes value using base64.

        :param key: bytes value to be encoded
        :type key: bytes
        :return: the encoded string
        :rtype: str
        """
        pass

    @classmethod
    def base58_decode(cls, key: str) -> bytes:
        """
        Decodes a string value encoded with base58.

        :param key: string value to be decoded
        :type key: str
        :return: the decoded bytes
        :rtype: bytes
        """
        pass

    @classmethod
    def base58_encode(cls, key: bytes) -> str:
        """
        Encodes a bytes value using base58.

        :param key: bytes value to be encoded
        :type key: bytes
        :return: the encoded string
        :rtype: str
        """
        pass

    @classmethod
    def base58_check_decode(cls, key: str) -> bytes:
        """
        Converts the specified str, which encodes binary data as base-58 digits, to an equivalent bytes value. The encoded
        str contains the checksum of the binary data.

        :param key: string value to be decoded
        :type key: str
        :return: the decoded bytes
        :rtype: bytes
        """
        pass

    @classmethod
    def base58_check_encode(cls, key: bytes) -> str:
        """
        Converts a bytes value to its equivalent str representation that is encoded with base-58 digits. The encoded str
        contains the checksum of the binary data.

        :param key: bytes value to be encoded
        :type key: bytes
        :return: the encoded string
        :rtype: str
        """
        pass

    @classmethod
    def itoa(cls, value: int, base: int = 10) -> str:
        """
        Converts the specific type of value to a decimal or hexadecimal string. The default is decimal.

        :param value: the int value
        :type value: int
        :param base: the value's base
        :type base: int
        :return: the converted string
        :rtype: int
        """
        pass

    @classmethod
    def atoi(cls, value: str, base: int = 10) -> int:
        """
        Converts a character string to a specific base value, decimal or hexadecimal. The default is decimal.

        :param value: the int value as a string
        :type value: str
        :param base: the value base
        :type base: int
        :return: the equivalent value
        :rtype: int

        :raise Exception: raised when base isn't 10 or 16.
        """
        pass

    @classmethod
    def memory_compare(cls, mem1: ByteString, mem2: ByteString) -> int:
        """
        Compares a memory with another one.

        :param mem1: a memory to be compared to another one
        :type mem1: bytes or str
        :param mem2: a memory that will be compared with another one
        :type mem2: bytes or str

        :return: -1 if mem1 precedes mem2, 0 if mem1 and mem2 are equal, 1 if mem1 follows mem2
        :rtype: int
        """
        pass

    @classmethod
    def memory_search(cls, mem: ByteString, value: ByteString, start: int = 0, backward: bool = False) -> int:
        """
        Searches for a given value in a given memory.

        :param mem: the memory
        :type mem: bytes or str
        :param value: the value
        :type value: bytes or str
        :param start: the index the search should start from
        :type start: int
        :param backward: whether it should invert the memory
        :type backward: bool

        :return: the index of the value in the memory. Returns -1 if it's not found
        :rtype: int
        """
        pass
