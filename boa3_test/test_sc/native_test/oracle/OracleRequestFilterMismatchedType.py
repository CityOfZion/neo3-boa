from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import OracleContract


@public
def oracle_call(url: str, callback: str, user_data: Any, gas_for_response: int):
    OracleContract.request(url, 1234, callback, user_data, gas_for_response)
