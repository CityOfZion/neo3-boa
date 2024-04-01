from typing import Any, List

from boa3.builtin.compile_time import public
from boa3.builtin.interop import storage
from boa3.builtin.interop.oracle import OracleResponseCode
from boa3.builtin.interop.stdlib import serialize
from boa3.builtin.nativecontract.oracle import Oracle
from boa3.builtin.type import helper as type_helper


@public
def oracle_call(url: str, request_filter: str, callback: str, user_data: Any, gas_for_response: int) -> bool:
    Oracle.request(url, request_filter, callback, user_data, gas_for_response)
    return True


@public
def callback_method(requested_url: str, user_data: bytes, code: OracleResponseCode, request_result: bytes):
    storage.put_str(b'pUrl', requested_url)
    storage.put(b'pUser', serialize(user_data))
    storage.put_int(b'pCode', code)
    storage.put(b'pRes', request_result)


@public
def get_storage() -> List[Any]:
    a = storage.get_str(b'pUrl')
    b = storage.get(b'pUser')
    c = storage.get_int(b'pCode')
    d = storage.get(b'pRes')

    return [a, b, c, d]
