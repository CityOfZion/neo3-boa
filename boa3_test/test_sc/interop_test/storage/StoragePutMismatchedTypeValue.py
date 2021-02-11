from boa3.builtin.interop.storage import put


def Main(key: bytes):
    value: list = [1, 2, 3]
    put(key, value)
