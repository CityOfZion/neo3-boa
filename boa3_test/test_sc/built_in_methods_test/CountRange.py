from boa3.builtin import public


@public
def main() -> int:
    return range(10).count(1)
