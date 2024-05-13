from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import OracleContract


@public
def oracle_call(url: str, request_filter: str, callback: str, user_data: Any):
    OracleContract.request(url, request_filter, callback, user_data, 'invalid_gas')
