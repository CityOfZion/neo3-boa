from boa3.builtin.compile_time import public


@public
def main(a: bytearray) -> bytearray:

    m = a[1:2]

    return m
