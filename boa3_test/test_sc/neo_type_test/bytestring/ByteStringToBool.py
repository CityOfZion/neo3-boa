from boa3.builtin.type import ByteString


def to_bool(arg: ByteString) -> bool:
    return arg.to_bool()
