from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.runtime import notify
from boa3.builtin.interop.storage import get, put


@public
def main() -> str:
    return get('storage').to_str()


@public
def _deploy(data: Any, update: bool):
    notify(update)
    notify(data)
    if isinstance(data, str):
        put('storage', data)
