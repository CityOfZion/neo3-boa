from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import get_context, put


@public
def Main(key: bytes):
    context = get_context()
    value: bytes = b'\x01\x02\x03'
    put(key, value, context)
