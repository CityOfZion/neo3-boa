def create_custom_id(value: str, use_time: bool = True) -> str:
    import platform

    suffix = platform.python_version()
    if use_time:
        import time
        suffix = f'{time.time_ns()}_{suffix}'

    if not isinstance(value, str) or len(value) == 0 or value.isspace():
        return suffix

    return f'{value}_{suffix}'
