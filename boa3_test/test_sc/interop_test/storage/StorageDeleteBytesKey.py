from boa3.builtin import public
from boa3.builtin.interop.storage import delete


@public
def Main(key: bytes):
    delete(key)
