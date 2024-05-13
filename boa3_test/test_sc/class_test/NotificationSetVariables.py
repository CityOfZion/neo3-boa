from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.types import UInt160, Notification


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
def state(obj: tuple[Any, ...]) -> Any:
    x = Notification()
    x.state = obj
    return x.state
