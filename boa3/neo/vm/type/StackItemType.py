from enum import Enum


class StackItemType(bytes, Enum):
    Any = b'\x00'
    Pointer = b'\x10'
    Boolean = b'\x20'
    Integer = b'\x21'
    ByteString = b'\x28'
    Buffer = b'\x30'
    Array = b'\x40'
    Struct = b'\x41'
    Map = b'\x48'
    InteropInterface = b'\x60'
