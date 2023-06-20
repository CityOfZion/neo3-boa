from boa3.builtin.interop.stdlib import memory_compare


def main(mem1: bytes) -> int:
    return memory_compare(mem1)
