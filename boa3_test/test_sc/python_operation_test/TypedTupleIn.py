from boa3.sc.compiletime import public


@public
def main(value: int, some_tuple: tuple[int]) -> bool:
    return value in some_tuple
