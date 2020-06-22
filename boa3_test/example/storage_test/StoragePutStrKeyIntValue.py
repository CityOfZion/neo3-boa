from boa3.interop.storage import put


def Main(key: str):
    value: int = 123
    put(key, value)
