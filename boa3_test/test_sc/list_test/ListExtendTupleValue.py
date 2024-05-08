from boa3.builtin.compile_time import public


@public
def Main() -> list[int]:
    a = [1, 2, 3]
    a.extend((4, 5, 6))
    return a  # expected [1, 2, 3, 4, 5, 6]
