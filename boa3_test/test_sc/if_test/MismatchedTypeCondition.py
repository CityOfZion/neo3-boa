def Main(condition: str) -> int:
    a = 0

    if condition:  # expecting bool, not str
        a = a + 2

    return a
