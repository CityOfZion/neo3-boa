from typing import Any, cast

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
        data_list[data.value[0]] = StdLib.deserialize(cast(bytes, data.value[1]))
    return data_list
