from boa3.sc.compiletime import public
from boa3.sc.storage import put


@public
def Main(key: bytes):
    value: bytes = b'\x01\x02\x03'
    put(key, value)
