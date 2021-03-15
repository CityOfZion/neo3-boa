from typing import Union

from boa3.builtin import public
from boa3.builtin.interop.storage import get, get_context


@public
def Main(key: Union[bytes, str]) -> bytes:
    context = get_context()
    return get(key, context)
