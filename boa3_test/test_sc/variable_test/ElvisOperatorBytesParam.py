from boa3.builtin.compile_time import public


@public
def main(param: bytes) -> bytes:
    other = param or b"some default value"
    return other
