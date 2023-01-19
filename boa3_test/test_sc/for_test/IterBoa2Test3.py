from boa3.builtin.compile_time import public


@public
def main() -> int:

    items = [0, 1, 2]

    count = 0

    for i in items:

        count += i

        if i == 1:
            print("ONE!")

            count += what()

        else:
            count -= minus(i)

    return count


def what() -> int:

    return 8


def minus(a: int) -> int:
    return a + 1
