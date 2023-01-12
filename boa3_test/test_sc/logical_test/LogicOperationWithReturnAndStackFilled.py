from boa3.builtin.compile_time import public


@public
def main() -> bool:
    test_var = True and return_inside_for()

    return test_var


def return_inside_for() -> bool:
    for number in [1, 10, 3]:
        if number == 10:
            return True
        elif number > 2:
            return True
    return False
