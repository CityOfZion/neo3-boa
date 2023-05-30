from boa3.builtin.compile_time import public
from boa3.builtin.contract import to_script_hash


@public
def Main() -> bytes:
    return to_script_hash('NUnLWXALK2G6gYa7RadPLRiQYunZHnncxg ')


@public
def Main2() -> bytes:
    return to_script_hash('123')
