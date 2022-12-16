from boa3.builtin.compile_time import public


@public
def main() -> int:

    count = 0

    for i in range(0, 12):
        count += 1

    return count
