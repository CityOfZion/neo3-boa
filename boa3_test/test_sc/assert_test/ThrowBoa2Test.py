from boa3.sc.compiletime import public


@public
def main(j: int) -> bool:

    assert j != 4

    return True
