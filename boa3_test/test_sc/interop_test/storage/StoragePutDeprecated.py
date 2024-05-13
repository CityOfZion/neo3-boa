from boa3.sc.compiletime import public
from boa3.builtin.interop.storage import put_int


@public
def Main(key: bytes):
    value: int = 123
    put_int(key, value)
