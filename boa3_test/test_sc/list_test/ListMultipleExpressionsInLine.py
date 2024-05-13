from boa3.sc.compiletime import public


@public
def Main(items1: list[int]) -> int:
    items2 = [False, '1', 2, 3, '4']; value = items1[0]; count = value + len(items2)
    return count
