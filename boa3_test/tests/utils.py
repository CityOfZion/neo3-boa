import base58


def create_custom_id(value: str, use_time: bool = True) -> str:
    import platform

    suffix = '_'.join(platform.python_version_tuple())
    if use_time:
        import time
        suffix = f'{time.time_ns()}_{suffix}'

    if not isinstance(value, str) or len(value) == 0 or value.isspace():
        return suffix

    return f'{value}_{suffix}'


def address_from_script_hash(script_hash: bytes, account_version: int) -> str:
    data = bytearray(script_hash)
    data.insert(0, account_version)

    return base58.b58encode_check(data).decode(encoding='utf-8')
