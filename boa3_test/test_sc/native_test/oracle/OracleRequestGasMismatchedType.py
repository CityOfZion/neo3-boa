from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.oracle import Oracle


@public
def oracle_call(url: str, request_filter: str, callback: str, user_data: Any):
    Oracle.request(url, request_filter, callback, user_data, 'invalid_gas')
