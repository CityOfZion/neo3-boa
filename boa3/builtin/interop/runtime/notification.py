__all__ = ['Notification']

from boa3.builtin.type import UInt160
from boa3.internal.deprecation import deprecated


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.types` instead')
class Notification:
    """
    Represents a notification.

    :ivar script_hash: the script hash of the notification sender
    :vartype script_hash: boa3.builtin.type.UInt160
    :ivar event_name: the notification's name
    :vartype event_name: str
    :ivar state: a tuple value storing all the notification contents.
    :vartype state: tuple
    """

    def __init__(self):
        self.script_hash: UInt160 = UInt160()
        self.event_name: str = ''
        self.state: tuple = ()
