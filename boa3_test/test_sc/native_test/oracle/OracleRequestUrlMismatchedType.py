from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.oracle import Oracle


@public
def oracle_call(request_filter: str, callback: str, user_data: Any, gas_for_response: int):
    Oracle.request(1234, request_filter, callback, user_data, gas_for_response)
