from boa3.builtin.compile_time import public


@public
def main() -> bytearray:

    m = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08')

    s2 = m[:4]

    return s2
