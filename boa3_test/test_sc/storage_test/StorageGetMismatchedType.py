from boa3.sc.storage import get


def Main(key: int) -> bytes:
    return get(key)
