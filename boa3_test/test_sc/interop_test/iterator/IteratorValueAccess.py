from typing import Any, cast

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
        data_list[data.value[0]] = StdLib.deserialize(cast(bytes, data.value[1]))
    return data_list
