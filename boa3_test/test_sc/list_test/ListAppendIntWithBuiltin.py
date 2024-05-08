from boa3.builtin.compile_time import public


@public
def Main() -> list[int]:
    a = [1, 2, 3]
    list.append(a, 4)
    return a
