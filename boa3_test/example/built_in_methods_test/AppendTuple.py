def Main(op: str, args: List[str]) -> List[int]:
    a = (1, 2, 3)
    a.append(4)  # compiler error - cannot append values to a tuple
    return a
