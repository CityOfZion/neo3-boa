from typing import Any, cast

from boa3.sc import storage
from boa3.sc.compiletime import public
from boa3.sc.types import FindOptions
from boa3.sc.utils.iterator import Iterator


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
    return storage.find(prefix, options=FindOptions.VALUES_ONLY)
