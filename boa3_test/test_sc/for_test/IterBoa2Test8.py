from boa3.builtin import public


@public
def main() -> int:
    rangestart = 2
    count = 0

    for i in range(rangestart, getrangeend()):
        count += 1

    return count


def getrangeend() -> int:
    return 8
