from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.runtime import get_notifications, notify
from boa3.sc.types import UInt160, Notification


@public
def with_param(args: list[Any], key: UInt160) -> list[Notification]:
    notify_args(args)
    return get_notifications(key)


@public
def without_param(args: list[Any]) -> list[Notification]:
    notify_args(args)
    return get_notifications()


def notify_args(args: list[Any]):
    for x in args:
        notify(x)
