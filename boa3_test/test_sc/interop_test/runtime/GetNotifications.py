from typing import Any, List

from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import Notification, get_notifications, notify
from boa3.builtin.type import UInt160


@public
def with_param(args: List[Any], key: UInt160) -> List[Notification]:
    notify_args(args)
    return get_notifications(key)


@public
def without_param(args: List[Any]) -> List[Notification]:
    notify_args(args)
    return get_notifications()


def notify_args(args: List[Any]):
    for x in args:
        notify(x)
