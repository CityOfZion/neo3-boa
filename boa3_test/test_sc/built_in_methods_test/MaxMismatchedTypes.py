from boa3.builtin import public


@public
def main() -> int:
    return max(123, '123')
