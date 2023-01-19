from boa3.builtin.compile_time import public


@public
def Main(a: bytes) -> bytes:
    return bytes.to_script_hash(a)
