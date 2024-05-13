from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import OracleContract


@public
def oracle_call(request_filter: str, callback: str, user_data: Any, gas_for_response: int):
    OracleContract.request(1234, request_filter, callback, user_data, gas_for_response)
