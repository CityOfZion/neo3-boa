from boa3.builtin.compile_time import public


@public
def main() -> bytes:
    c = b'\x01\x04\xaf\x09'

    l = len(c)

    b = c[2:1]

    j = b'\x01\x02\x03\x04\x05\x06\x07'

    k = c + j

    m = k[3:6]

    return m + b
