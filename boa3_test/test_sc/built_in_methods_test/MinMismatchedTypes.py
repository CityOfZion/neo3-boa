from boa3.builtin import public


@public
def main() -> int:
    return min(10, 'test')
