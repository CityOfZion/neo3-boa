from boa3.builtin import public


@public
def main(x: str) -> int:
    return sum(x)
