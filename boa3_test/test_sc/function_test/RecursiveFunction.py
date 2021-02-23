from boa3.builtin import public


def fact(f: int) -> int:
    if f <= 1:
        return 1
    return f * fact(f - 1)


@public
def main() -> int:
    return fact(57)
