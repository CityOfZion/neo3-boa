from boa3.sc.storage import get


def Main(key: str) -> bytes:
    return get(key)
