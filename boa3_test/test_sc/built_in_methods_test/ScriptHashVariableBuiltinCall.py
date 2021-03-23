from boa3.builtin import public


@public
def Main(a: bytes) -> bytes:
    return bytes.to_script_hash(a)
