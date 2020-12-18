def fact(f: int) -> int:
    if f <= 1:
        return 1
    return f * fact(f - 1)


def main() -> int:
    print(fact(150))
