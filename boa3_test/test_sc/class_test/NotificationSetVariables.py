from typing import Any, Tuple

from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import Notification
from boa3.builtin.type import UInt160


@public
def script_hash(script: UInt160) -> bytes:
    x = Notification()
    x.script_hash = script
    return x.script_hash


@public
def event_name(event: str) -> str:
    x = Notification()
    x.event_name = event
    return x.event_name


@public
def state(obj: Tuple[Any]) -> Any:
    x = Notification()
    x.state = obj
    return x.state
