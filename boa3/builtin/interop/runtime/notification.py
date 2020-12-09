from typing import Any, Tuple

from boa3.builtin.type import UInt160


class Notification:
    def __init__(self):
        self.script_hash: UInt160 = UInt160()
        self.event_name: str = ''
        self.state: Tuple[Any] = ()
