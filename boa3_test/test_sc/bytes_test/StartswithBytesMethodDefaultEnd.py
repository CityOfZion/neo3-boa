
from boa3.sc.compiletime import public


@public
def main(bytes_value: bytes, subbytes_value: bytes, start: int) -> bool:
    return bytes_value.startswith(subbytes_value, start)
