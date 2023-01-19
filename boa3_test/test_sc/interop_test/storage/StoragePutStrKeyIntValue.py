from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import put


@public
def Main(key: str):
    value: int = 123
    put(key, value)
