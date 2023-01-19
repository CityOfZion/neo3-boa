from boa3.builtin.compile_time import public


@public
def main() -> bytes:

    items = [0, 1, 2]

    items2 = ['a', 'b', 'c', 'd']
    count = 0

    blah = b''

    for i in items:

        for j in items2:

            blah = blah + j

            count += 1

    blah = blah + count

    return blah
