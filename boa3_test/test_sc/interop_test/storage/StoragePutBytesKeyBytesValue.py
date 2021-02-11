from boa3.builtin import public
from boa3.builtin.interop.storage import put


@public
def Main(key: bytes):
    value: bytes = b'\x01\x02\x03'
    put(key, value)
