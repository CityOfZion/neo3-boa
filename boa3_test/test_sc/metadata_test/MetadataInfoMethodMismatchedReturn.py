from boa3.builtin.compile_time import metadata


def Main() -> int:
    return 5


@metadata
def manifest() -> int:
    return 5
