from boa3.builtin.compile_time import public


@public
def Main(a: bytes) -> bytes:
    return a.to_script_hash()
