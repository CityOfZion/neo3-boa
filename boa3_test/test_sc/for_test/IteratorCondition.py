from typing import Any, cast

from boa3.builtin.compile_time import public
from boa3.builtin.interop.iterator import Iterator
from boa3.sc import storage


@public
def Main() -> int:
    value = get_iterator()
    a: int = 0

    for x in value:
        a = a + cast(int, x)

    return a


@public
def _deploy(data: Any, update: bool):
    prefix = b'example'
    storage.put_int(prefix + b'\x01', 1)
    storage.put_int(prefix + b'\x02', 2)
    storage.put_int(prefix + b'\x03', 3)


def get_iterator() -> Iterator:
    prefix = b'example'
    return storage.find(prefix, options=storage.FindOptions.VALUES_ONLY)
