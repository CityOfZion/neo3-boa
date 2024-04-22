def Main(op: str, args: list) -> tuple[int]:
    a = (1, 2, 3)
    a.extend([4, 5, 6])  # compiler error - tuples are immutables
    return a
