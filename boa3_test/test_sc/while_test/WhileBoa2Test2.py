from boa3.builtin.compile_time import public


@public
def Main() -> int:

    j = 3
    while j < 8:
        j = j + 1

        if j == 6:
            break

    return j
