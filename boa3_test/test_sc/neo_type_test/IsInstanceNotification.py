from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import Notification, get_notifications, notify


@public
def is_notification(value: Any) -> bool:
    return isinstance(value, Notification)


@public
def get_notifications_is_notification() -> bool:
    notify("unit_test")

    n = get_notifications()

    if len(n) > 0:
        return is_notification(n[0])
    else:
        return False
