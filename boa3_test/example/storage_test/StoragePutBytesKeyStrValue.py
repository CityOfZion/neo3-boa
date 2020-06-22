from boa3.interop.storage import put


def Main(key: bytes):
    value: str = '123'
    put(key, value)
