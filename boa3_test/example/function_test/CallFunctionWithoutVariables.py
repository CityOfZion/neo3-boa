def One() -> int:
    return 1


def Main(number: int) -> int:
    if number == 1:
        return One()
    elif number == 2:
        return Two()
    return 0


def Two() -> int:
    return 1 + One()
