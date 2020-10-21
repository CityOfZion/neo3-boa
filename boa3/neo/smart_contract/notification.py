from typing import Any, Dict


class Notification:
    def __init__(self, event_name: str, script_hash: bytes, value: Any = None):
        self._event_name: str = event_name
        self._script_hash: bytes = script_hash
        self._value: Any = value

    @classmethod
    def from_json(cls, json: Dict[str, Any]):
        """
        Creates a Notification object from a json.

        :param json: json that contains the notification data
        :return: a Notification object
        :rtype: Notification
        """
        name: str = json["eventName"] if "eventName" in json else ""
        script: bytes = json["scriptHash"] if "scriptHash" in json else b''
        value: Any = json["value"] if "value" in json else None

        return cls(name, script, value)
