from boa3.sc.compiletime import public


@public
def Main(items1: tuple[int, ...]) -> int:
    items2 = ('a', 'b', 'c', 'd'); value = items1[0]; count = value + len(items2)
    return count
