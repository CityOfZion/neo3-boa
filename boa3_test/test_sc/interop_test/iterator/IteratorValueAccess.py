from typing import Any, cast

from boa3.builtin import public
from boa3.builtin.interop import storage
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def store(prefix: str, value: Any):
    serialized_value = StdLib.serialize(value)
    storage.put(prefix, serialized_value)


@public
def search_storage(prefix: str) -> dict:
    data_list = {}
    data = storage.find(prefix)

    while data.next():
        data_list[data.value[0]] = StdLib.deserialize(cast(bytes, data.value[1]))
    return data_list
