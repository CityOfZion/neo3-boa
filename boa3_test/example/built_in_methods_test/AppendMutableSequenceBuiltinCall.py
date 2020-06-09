def Main(op: str, args: List[str]) -> MutableSequence[int]:
    a: MutableSequence[Any] = [1, 2, 3]
    MutableSequence.append(a, 4)
    return a
