from boa3.builtin.compile_time import public


@public
def Main(number: int) -> int:
    # the function has a return to each condition
    if number % 3 == 1:
        return number - 1
    elif number % 3 == 2:
        return number + 1
    else:
        return number
