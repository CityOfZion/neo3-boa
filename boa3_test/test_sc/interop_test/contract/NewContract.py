from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import notify
from boa3.builtin.interop.storage import get_str, put_str


@public
def main() -> str:
    return get_str(b'storage')


@public
def _deploy(data: Any, update: bool):
    notify(update)
    notify(data)
    if isinstance(data, str):
        put_str(b'storage', data)
