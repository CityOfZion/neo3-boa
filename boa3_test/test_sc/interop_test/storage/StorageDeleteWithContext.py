from typing import Union

from boa3.builtin import public
from boa3.builtin.interop.storage import delete, get_context


@public
def Main(key: Union[bytes, str]):
    context = get_context()
    delete(key, context)
