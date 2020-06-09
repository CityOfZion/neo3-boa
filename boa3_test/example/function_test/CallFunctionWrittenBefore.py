def TestAdd(a: int, b: int) -> int:
    return a + b


def Main(operation: str, args: Tuple[int]) -> int:
    if operation == 'TestAdd':
        return TestAdd(1, 2)
