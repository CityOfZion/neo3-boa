from typing import Any

from boa3.sc import runtime
from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def symbol() -> str:
    return "test"


def get_id() -> str:
    return StdLib.itoa(runtime.get_random())


@public
def Main() -> Any:
    token_id = get_id()
    first_token = {"id": token_id, "name": (symbol() + token_id)}
    return first_token
