from boa3.builtin import public


@public
def main() -> int:
    a = ['unit', 'test', 'unit', 'unit', 'random', 'string']
    return a.count('unit')
