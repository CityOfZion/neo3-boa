from boa3.sc.compiletime import public


@public
def main(a: int | None) -> bool:
    if a is None:
        return True
    else:
        return some_function(a)


def some_function(var: int) -> bool:
    return False
