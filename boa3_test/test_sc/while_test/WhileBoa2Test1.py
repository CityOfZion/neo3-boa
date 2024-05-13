from boa3.sc.compiletime import public


@public
def Main() -> int:

    j = 3
    while j < 6:
        j = j + 1

    return j
