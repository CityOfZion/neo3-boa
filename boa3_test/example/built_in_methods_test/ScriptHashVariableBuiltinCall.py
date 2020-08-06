def Main() -> bytes:
    a = '123'
    return str.to_script_hash(a)  # only works with literals
