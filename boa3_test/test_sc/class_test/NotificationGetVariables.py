from typing import Any, List

from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import Notification, executing_script_hash, get_notifications, notify


@public
def script_hash(args: List[Any]) -> bytes:
    return notification(args).script_hash


@public
def event_name(args: List[Any]) -> str:
    return notification(args).event_name


@public
def state(args: List[Any]) -> Any:
    return notification(args).state


def notification(args: List[Any]) -> Notification:
    for x in args:
        notify(x)

    n = get_notifications(executing_script_hash)

    if len(n) > 0:
        return n[0]
    return Notification()
