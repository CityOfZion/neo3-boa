from boa3.sc.compiletime import public


@public
def fun_with_starred(*args: int) -> int:
    return len(args)


@public
def main(list_with_args: list[int]) -> int:
    return fun_with_starred(*list_with_args)
