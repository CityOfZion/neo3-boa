from boa3.sc.compiletime import public


@public
def main() -> int:

    items = ['a', 'b', 'c', 1, 5]

    count = 3
    for i in items:

        count += 1

    return count
