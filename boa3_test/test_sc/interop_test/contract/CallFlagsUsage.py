from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.utils import call_contract
from boa3.sc.runtime import executing_script_hash, notify
from boa3.sc.storage import get_int, put_int


@public
def call_another_contract() -> Any:
    return call_contract(NeoToken.hash, 'balanceOf', [executing_script_hash])


@public
def notify_user():
    notify('Notify was called')


@public
def put_value(key: bytes, value: int):
    put_int(key, value)


@public
def get_value(key: bytes) -> int:
    return get_int(key)
