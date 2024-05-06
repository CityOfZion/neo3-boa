from typing import Any, Self

from boa3.internal.neo import to_hex_str
from boa3.internal.neo3.core.types import UInt160


class TestRunnerLog:
    _contract_key = 'contract'
    _message_key = 'message'

    def __init__(self, script_hash: bytes, message: str):
        self._script_hash: bytes = script_hash
        self._message: str = message

    @property
    def origin(self) -> bytes:
        return self._script_hash

    @property
    def message(self) -> str:
        return self._message

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        """
        Creates a Log object from a json.

        :param json: json that contains the log data
        :return: a Log object
        :rtype: TestRunnerLog
        """
        keys = set(json.keys())
        if not keys.issubset([cls._contract_key, cls._message_key]):
            return None

        script: bytes = json[cls._contract_key] if cls._contract_key in json else b''
        message: str = json[cls._message_key] if cls._message_key in json else ""

        if isinstance(script, str):
            script = UInt160.from_string(script[2:]
                                         if script.startswith('0x')
                                         else script
                                         ).to_array()

        return cls(script, message)

    def __str__(self) -> str:
        return '[{0}] {1}'.format(to_hex_str(self.origin), self._message)

    def __repr__(self) -> str:
        return str(self)
