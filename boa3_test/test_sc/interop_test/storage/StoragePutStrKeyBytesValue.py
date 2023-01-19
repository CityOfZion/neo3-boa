from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import put


@public
def Main(key: str):
    value: bytes = b'\x01\x02\x03'
    put(key, value)
