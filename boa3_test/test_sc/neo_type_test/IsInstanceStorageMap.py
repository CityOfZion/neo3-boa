from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import StorageMap, get_context


@public
def is_storage_map(value: Any) -> bool:
    return isinstance(value, StorageMap)


@public
def create_map_is_storage_map() -> Any:
    storage_map = get_context().create_map(b'example_')
    return is_storage_map(storage_map)
