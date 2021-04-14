from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.contract import call_contract, NEO
from boa3.builtin.interop.runtime import notify, executing_script_hash
from boa3.builtin.interop.storage import get, put


@public
def call_another_contract() -> Any:
    return call_contract(NEO, 'balanceOf', [executing_script_hash])


@public
def notify_user():
    notify('Notify was called')


@public
def put_value(key: str, value: int):
    put(key, value)


@public
def get_value(key: str) -> int:
    return get(key).to_int()
