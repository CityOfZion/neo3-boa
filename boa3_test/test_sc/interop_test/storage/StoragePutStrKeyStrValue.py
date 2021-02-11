from boa3.builtin import public
from boa3.builtin.interop.storage import put


@public
def Main(key: str):
    value: str = '123'
    put(key, value)
