from boa3.interop.storage import get


def Main(key: int) -> bytes:
    return get(key)
