from boa3.sc.storage import put_str


def Main(key: str):
    value: str = '123'
    put_str(key, value)
