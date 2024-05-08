from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import put_str


@public
def Main(key: bytes):
    value: str = '123'
    put_str(key, value)
