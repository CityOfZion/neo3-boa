from boa3.interop.storage import get


def Main(key: bytes) -> bytes:
    return get(key)
