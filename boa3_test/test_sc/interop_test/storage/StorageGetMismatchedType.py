from boa3.builtin.interop.storage import get


def Main(key: int) -> bytes:
    return get(key)
