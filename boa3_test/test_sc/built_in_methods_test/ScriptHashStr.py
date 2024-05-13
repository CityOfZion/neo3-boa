from boa3.sc.compiletime import public
from boa3.sc.utils import to_script_hash


@public
def Main() -> bytes:
    return to_script_hash('NUnLWXALK2G6gYa7RadPLRiQYunZHnncxg ')


@public
def Main2() -> bytes:
    return to_script_hash('123')
