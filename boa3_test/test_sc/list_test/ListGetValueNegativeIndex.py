from boa3.builtin.compile_time import public


@public
def Main(a: list[int]) -> int:
    return a[-1]  # raises runtime error if the list is empty
