from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib
from boa3.sc import storage


@public
def store(prefix: bytes, value: Any):
    storage.put_object(prefix, value)


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
