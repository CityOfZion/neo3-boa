from boa3.builtin.compile_time import public


@public
def main() -> tuple[int, int, int]:
    a = (b'unit', 'test', b'unit', b'unit', 123, 123, True, False)
    b: tuple[int, int, int] = (a.count(b'unit'), a.count('test'), a.count(123))
    return b
