from boa3.sc.compiletime import public


@public
def Main() -> list[int]:
    a = [1, 2, 3]
    list.insert(a, 2, 4)
    return a  # expected [1, 2, 4, 3]
