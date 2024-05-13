from boa3.sc.compiletime import public
from boa3.sc.storage import put_str


@public
def Main(key: bytes):
    value: str = '123'
    put_str(key, value)
