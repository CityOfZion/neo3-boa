from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import delete, get_context
from boa3.builtin.type import ByteString


@public
def Main(key: ByteString):
    context = get_context()
    delete(key, context)
