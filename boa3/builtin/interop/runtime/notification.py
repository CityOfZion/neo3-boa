from typing import Any, Tuple


class Notification:
    def __init__(self):
        self.script_hash: bytes = bytes()
        self.event_name: str = ''
        self.state: Tuple[Any] = ()
