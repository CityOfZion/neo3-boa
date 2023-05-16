from boa3.builtin.compile_time import public


@public
def main(x: int, y: int) -> list:
    return [0, 1, 2, 3, 4, 5][x:y]
