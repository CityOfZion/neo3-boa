from boa3.builtin import public


@public
def Main() -> bytes:
    return int.to_script_hash(123)
