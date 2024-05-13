from typing import Any

from boa3.sc import contracts
from boa3.sc.compiletime import public
from boa3.sc.types import OracleResponseCode


@public
def oracle_call(url: str, request_filter: str, callback: str, user_data: Any, gas_for_response: int):
    contracts.OracleContract.request(url, request_filter, callback, user_data, gas_for_response)


@public
def test_callback(requested_url: str, user_data: Any, code: int, request_result: OracleResponseCode):
    return
