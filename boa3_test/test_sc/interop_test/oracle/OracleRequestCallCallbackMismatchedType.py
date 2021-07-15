from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.oracle import Oracle


@public
def oracle_call(url: str, request_filter: str, user_data: Any, gas_for_response: int):
    Oracle.request(url, request_filter, 1234, user_data, gas_for_response)
