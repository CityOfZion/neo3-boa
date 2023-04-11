from __future__ import annotations

from typing import Any, Dict, Tuple

from boa3.internal.neo import to_hex_str
from boa3.internal.neo.utils import stack_item_from_json


class Notification:
    _event_name_key = 'eventname'
    _script_hash_key = 'scripthash'
    _value_key = 'value'

    def __init__(self, event_name: str, script_hash: bytes, *value: Any):
        self._event_name: str = event_name
        self._script_hash: bytes = script_hash
        self._value: Tuple[Any] = value

    @property
    def name(self) -> str:
        return self._event_name

    @property
    def origin(self) -> bytes:
        return self._script_hash

    @property
    def arguments(self) -> tuple:
        return self._value

    @classmethod
    def from_json(cls, json: Dict[str, Any], *args, **kwargs) -> Notification:
        """
        Creates a Notification object from a json.

        :param json: json that contains the notification data
        :return: a Notification object
        :rtype: Notification
        """
        keys = set(json.keys())
        if not keys.issubset([cls._event_name_key, cls._script_hash_key, cls._value_key]):
            return None

        name: str = json[cls._event_name_key] if cls._event_name_key in json else ""
        script: bytes = json[cls._script_hash_key] if cls._script_hash_key in json else b''
        try:
            value: Any = stack_item_from_json(json[cls._value_key]) if cls._value_key in json else []
        except ValueError:
            value = []

        if not isinstance(value, list):
            value = [value]

        if isinstance(script, str):
            script = cls._get_script_from_str(script)

        return cls(name, script, *value)

    @classmethod
    def _get_script_from_str(cls, script: str) -> bytes:
        if isinstance(script, str) and script.startswith('0x'):
            bytes_script = bytearray()
            for x in range(2, len(script), 2):
                bytes_script.append(int(script[x:x + 2], 16))
            bytes_script.reverse()
            script = bytes(bytes_script)
        return script

    def __str__(self) -> str:
        return '[{0}] {1}'.format(to_hex_str(self.origin), self._event_name)

    def __repr__(self) -> str:
        return str(self)
