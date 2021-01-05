from boa3.builtin.interop.storage import get


def Main(key: bytes) -> bytes:
    return get(key)
