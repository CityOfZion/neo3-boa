from boa3.builtin.compile_time import public


@public
def main(a: int, b: int, c: int, d: int) -> int:
    a2 = a * 2
    b2 = b + 1
    c2 = c // 2
    d2 = d - 1
    return a2 + b2 + c2 + d2
