from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import get, get_context
from boa3.builtin.type import ByteString


@public
def Main(key: ByteString) -> bytes:
    context = get_context()
    return get(key, context)
