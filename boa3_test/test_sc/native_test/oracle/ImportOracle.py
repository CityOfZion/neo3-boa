from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop import oracle


@public
def oracle_call(url: str, request_filter: str, callback: str, user_data: Any, gas_for_response: int):
    oracle.Oracle.request(url, request_filter, callback, user_data, gas_for_response)


@public
def test_callback(requested_url: str, user_data: Any, code: int, request_result: oracle.OracleResponseCode):
    return
