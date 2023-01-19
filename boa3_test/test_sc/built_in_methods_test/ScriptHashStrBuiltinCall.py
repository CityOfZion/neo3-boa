from boa3.builtin.compile_time import public


@public
def Main() -> bytes:
    return str.to_script_hash('123')
