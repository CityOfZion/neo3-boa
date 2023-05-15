from boa3.builtin.compile_time import public


@public
def Main(x: int, y: int) -> str:
    return 'unit_test'[x:y]
