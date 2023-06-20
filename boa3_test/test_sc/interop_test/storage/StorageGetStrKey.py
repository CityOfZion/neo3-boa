from boa3.builtin.interop.storage import get


def Main(key: str) -> bytes:
    return get(key)
