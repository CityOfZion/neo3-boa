from boa3.builtin import public


@public
def Main() -> bytes:
    return str.to_script_hash('123')
