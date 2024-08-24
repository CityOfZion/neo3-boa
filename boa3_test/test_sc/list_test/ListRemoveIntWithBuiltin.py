from boa3.sc.compiletime import public


@public
def Main() -> list[int]:
    a = [10, 20, 30]
    list.remove(a, 30)
    return a  # expected [10, 20]
