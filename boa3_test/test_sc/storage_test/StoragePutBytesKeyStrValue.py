from boa3.builtin import public
from boa3.builtin.interop.storage import put


@public
def Main(key: bytes):
    value: str = '123'
    put(key, value)
