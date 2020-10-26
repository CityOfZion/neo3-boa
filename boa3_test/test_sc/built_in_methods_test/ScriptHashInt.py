from boa3.builtin import public


@public
def Main() -> bytes:
    return (123).to_script_hash()
