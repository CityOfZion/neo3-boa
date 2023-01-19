from boa3.builtin.compile_time import public


@public
def main() -> bytes:
    return max(b'Lorem', b'ipsum', b'dolor', b'sit', b'amet')
