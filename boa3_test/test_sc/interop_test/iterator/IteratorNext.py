from typing import Collection

from boa3.builtin import public
from boa3.builtin.interop.iterator import Iterator


@public
def has_next(x: Collection) -> bool:
    return Iterator(x).next()
