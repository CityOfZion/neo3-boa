from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import notify
from boa3.builtin.interop.storage import get, put
from boa3.builtin.type.helper import to_str


@public
def main() -> str:
    return to_str(get('storage'))


@public
def _deploy(data: Any, update: bool):
    notify(update)
    notify(data)
    if isinstance(data, str):
        put('storage', data)
