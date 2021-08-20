from boa3.builtin import public


@public
def main() -> bytes:
    a = b'12345'
    return a[::2]
