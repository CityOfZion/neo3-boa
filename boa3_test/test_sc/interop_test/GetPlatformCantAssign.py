from boa3.builtin.interop.runtime import get_platform


def main(example: str) -> str:
    global get_platform
    get_platform = example
    return get_platform
