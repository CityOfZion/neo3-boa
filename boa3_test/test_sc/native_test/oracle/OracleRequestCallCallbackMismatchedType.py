from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.oracle import Oracle


@public
def oracle_call(url: str, request_filter: str, user_data: Any, gas_for_response: int):
    Oracle.request(url, request_filter, 1234, user_data, gas_for_response)
