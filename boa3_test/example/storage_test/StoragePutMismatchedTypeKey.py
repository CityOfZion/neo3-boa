from boa3.interop.storage import put


def Main(key: list):
    value: bytes = b'\x01\x02\x03'
    put(key, value)
