from boa3.builtin.type import ByteString


def to_bytes(arg: ByteString) -> bytes:
    return arg.to_bytes()
