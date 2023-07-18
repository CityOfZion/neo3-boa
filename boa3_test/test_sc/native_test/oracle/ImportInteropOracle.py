from typing import Any

from boa3.builtin import interop
from boa3.builtin.compile_time import public


@public
def oracle_call(url: str, request_filter: str, callback: str, user_data: Any, gas_for_response: int):
    interop.oracle.Oracle.request(url, request_filter, callback, user_data, gas_for_response)


@public
def test_callback(requested_url: str, user_data: Any, code: int, request_result: interop.oracle.OracleResponseCode):
    return
