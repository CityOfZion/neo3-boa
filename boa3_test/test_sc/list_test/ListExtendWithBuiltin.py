from boa3.sc.compiletime import public


@public
def Main() -> list[int]:
    a = [1, 2, 3]
    list.extend(a, [4, 5, 6])
    return a  # expected [1, 2, 3, 4, 5, 6]
