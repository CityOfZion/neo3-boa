from boa3.builtin.compile_time import public


@public
def main(j: int) -> bool:

    assert j != 4

    return True
