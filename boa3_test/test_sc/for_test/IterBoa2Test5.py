from boa3.sc.compiletime import public


@public
def main() -> int:

    items = [0, 1, 2]

    items2 = ['a', 'b', 'c', 'd']
    count = 0

    for i in items:  # 3

        count += 1

        for j in items2:  # 4

            count += 1

            for k in items:  # 3
                count += 1

    return count
