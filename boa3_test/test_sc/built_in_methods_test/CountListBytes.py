from boa3.builtin.compile_time import public


@public
def main() -> int:
    a = [b'unit', b'test', b'unit', b'unit', b'random', b'string']
    return a.count(b'unit')
