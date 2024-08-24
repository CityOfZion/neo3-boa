from typing import Any

from boa3.sc import storage
from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def store(prefix: bytes, value: Any):
    serialized_value = StdLib.serialize(value)
    storage.put(prefix, serialized_value)


@public
def search_storage(prefix: bytes) -> dict:
    data_list = {}
    data = storage.find(prefix)

    while data.next():
        iterator_value = data.value
        key: str = iterator_value[0]
        serialized_value: bytes = iterator_value[1]
        value = StdLib.deserialize(serialized_value)
        data_list[key] = value
    return data_list
