def Main(a: bytes) -> bytes:
    a[0] = 0x01  # compiler error - 'bytes' does not support item assignment
    return a
