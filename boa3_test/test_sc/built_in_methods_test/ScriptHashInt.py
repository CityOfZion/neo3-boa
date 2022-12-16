from boa3.builtin.compile_time import public


@public
def Main() -> bytes:
    return (123).to_script_hash()
