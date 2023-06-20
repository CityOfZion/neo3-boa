from boa3.builtin.interop.stdlib import memory_search


def main(mem: bytes) -> int:
    return memory_search(mem)
