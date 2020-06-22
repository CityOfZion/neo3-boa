from boa3.interop.storage import put


def Main(key: bytes):
    value: int = 123
    put(key, value)
