def Main(a: bytes) -> bytes:
    a[0] = 0x01
    return a
