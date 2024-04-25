from boa3.builtin.compile_time import public
from boa3.sc.storage import put_int


@public
def Main(key: bytes):
    value: int = 123
    put_int(key, value)
