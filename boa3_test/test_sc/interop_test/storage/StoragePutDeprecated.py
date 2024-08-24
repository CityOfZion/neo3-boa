from boa3.builtin.interop.storage import put_int
from boa3.sc.compiletime import public


@public
def Main(key: bytes):
    value: int = 123
    put_int(key, value)
