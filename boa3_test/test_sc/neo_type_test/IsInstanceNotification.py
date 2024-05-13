from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.runtime import get_notifications, notify
from boa3.sc.types import Notification


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
