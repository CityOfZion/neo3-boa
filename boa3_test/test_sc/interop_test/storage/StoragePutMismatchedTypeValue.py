from boa3.sc.storage import put


def Main(key: bytes):
    value: list = [1, 2, 3]
    put(key, value)
