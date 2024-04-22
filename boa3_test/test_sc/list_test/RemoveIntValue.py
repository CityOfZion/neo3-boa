from boa3.builtin.compile_time import public


@public
def Main() -> list[int]:
    a = [10, 20, 30]
    a.remove(20)
    return a  # expected [10, 30]
