from boa3.builtin.compile_time import public


@public
def Main() -> list[int]:
    a = [1, 2, 3]
    a.insert(2, 4)
    return a  # expected [1, 2, 4, 3]
