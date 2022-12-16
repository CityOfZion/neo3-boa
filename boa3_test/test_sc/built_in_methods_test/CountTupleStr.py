from boa3.builtin.compile_time import public


@public
def main() -> int:
    a = ('unit', 'test', 'unit', 'unit', 'random', 'string')
    return a.count('unit')
