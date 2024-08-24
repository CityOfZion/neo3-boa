from boa3.sc.compiletime import public


@public
def main(a: int | None) -> bool:
    if a is not None:
        return some_function(a)
    else:
        return False


def some_function(var: int) -> bool:
    return True
