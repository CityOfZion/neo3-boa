from boa3.sc.compiletime import public


@public
def main() -> int:

    items = range(0, 10)

    count = 0

    for i in items:
        count += 1

    return count
