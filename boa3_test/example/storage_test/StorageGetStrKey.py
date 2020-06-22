from boa3.interop.storage import get


def Main(key: str) -> bytes:
    return get(key)
