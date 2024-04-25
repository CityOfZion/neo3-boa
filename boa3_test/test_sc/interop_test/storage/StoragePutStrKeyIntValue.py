from boa3.sc.storage import put_int


def Main(key: str):
    value: int = 123
    put_int(key, value)
