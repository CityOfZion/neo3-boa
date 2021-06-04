from boa3.builtin.interop.runtime import platform


def main(example: str) -> str:
    global platform
    platform = example
    return platform
