__all__ = [
    'StdLib',
]


from typing import Any, Union

from boa3.builtin.type import UInt160


class StdLib:
    """
    A class used to represent StdLib native contract.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/native/StdLib>`__
    to learn more about the StdLib class.
    """

    hash: UInt160

    @classmethod
    def serialize(cls, item: Any) -> bytes:
        """
        Serializes the given value into its bytes representation.

        >>> StdLib.serialize('42')
        b'(\\x0242'

        >>> StdLib.serialize(42)
        b'!\\x01*'

        >>> StdLib.serialize([2, 3, 5, 7])
        b'@\\x04!\\x01\\x02!\\x01\\x03!\\x01\\x05!\\x01\\x07'

        >>> StdLib.serialize({1: 1, 2: 1, 3: 2})
        b'H\\x03!\\x01\\x01!\\x01\\x01!\\x01\\x02!\\x01\\x01!\\x01\\x03!\\x01\\x02'

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

        >>> StdLib.deserialize(b'(\\x0242')
        '42'

        >>> StdLib.deserialize(b'!\\x01*')
        42

        >>> StdLib.deserialize(b'@\\x04!\\x01\\x02!\\x01\\x03!\\x01\\x05!\\x01\\x07')
        [2, 3, 5, 7]

        >>> StdLib.deserialize(b'H\\x03!\\x01\\x01!\\x01\\x01!\\x01\\x02!\\x01\\x01!\\x01\\x03!\\x01\\x02')
        {1: 1, 2: 1, 3: 2}

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

        >>> StdLib.json_serialize({'one': 1, 'two': 2, 'three': 3})
        '{"one":1,"two":2,"three":3}'

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

        >>> StdLib.json_deserialize('{"one":1,"two":2,"three":3}')
        {'one': 1, 'three': 3, 'two': 2}

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

        >>> StdLib.base64_decode("dW5pdCB0ZXN0")
        b"unit test"

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

        >>> StdLib.base64_encode(b'unit test')
        b"dW5pdCB0ZXN0"

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

        >>> StdLib.base58_decode('2VhL46g69A1mu')
        b"unit test"

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

        >>> StdLib.base58_encode(b'unit test')
        b"2VhL46g69A1mu"

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

        >>> StdLib.base58_check_decode('AnJcKqvgBwKxsjX75o')
        b"unit test"

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

        >>> StdLib.base58_check_encode(b'unit test')
        b"AnJcKqvgBwKxsjX75o"

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

        >>> StdLib.itoa(10)
        '10'

        >>> StdLib.itoa(123)
        '123'

        >>> StdLib.itoa(-1, 16)
        'f'

        >>> StdLib.itoa(15, 16)
        '0f'

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

        >>> StdLib.atoi('10')
        10

        >>> StdLib.atoi('123')
        123

        >>> StdLib.atoi('1f', 16)
        31

        >>> StdLib.atoi('ff', 16)
        -1

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
    def memory_compare(cls, mem1: Union[bytes, str], mem2: Union[bytes, str]) -> int:
        """
        Compares a memory with another one.

        >>> StdLib.memory_compare('abc', 'abc')
        0

        >>> StdLib.memory_compare('ABC', 'abc')
        -1

        >>> StdLib.memory_compare('abc', 'ABC')
        1

        :param mem1: a memory to be compared to another one
        :type mem1: bytes or str
        :param mem2: a memory that will be compared with another one
        :type mem2: bytes or str

        :return: -1 if mem1 precedes mem2, 0 if mem1 and mem2 are equal, 1 if mem1 follows mem2
        :rtype: int
        """
        pass

    @classmethod
    def memory_search(cls, mem: Union[bytes, str], value: Union[bytes, str], start: int = 0, backward: bool = False) -> int:
        """
        Searches for a given value in a given memory.

        >>> StdLib.memory_search('abcde', 'a', 0)
        0

        >>> StdLib.memory_search('abcde', 'e', 0)
        4

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
