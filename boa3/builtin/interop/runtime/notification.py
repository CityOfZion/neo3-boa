from typing import Any, Tuple

from boa3.builtin.type import UInt160


class Notification:
    """
    Represents a notification.

    :var script_hash: the script hash of the notification sender
    :vartype script_hash: UInt160
    :var event_name: the notification's name
    :vartype event_name: str
    :var state: the object representing the notification content, which can be of any type such as value, string, array,
        etc
    :vartype state: tuple
    """
    def __init__(self):
        self.script_hash: UInt160 = UInt160()
        self.event_name: str = ''
        self.state: Tuple[Any] = ()
