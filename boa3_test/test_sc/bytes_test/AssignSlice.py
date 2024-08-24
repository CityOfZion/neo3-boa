from boa3.sc.compiletime import public


@public
def main(a: bytearray) -> bytearray:

    m = a[1:2]

    return m
