from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import StorageContext, get_context


@public
def is_context(value: Any) -> bool:
    return isinstance(value, StorageContext)


@public
def get_context_is_context() -> bool:
    context = get_context()
    return is_context(context)
