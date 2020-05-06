from enum import Enum


class AbiType(str, Enum):
    Signature = 'Signature'
    Boolean = 'Boolean'
    Integer = 'Integer'
    Hash160 = 'Hash160'
    Hash256 = 'Hash256'
    ByteArray = 'ByteArray'
    PublicKey = 'PublicKey'
    String = 'String'
    Array = 'Array'
    Map = 'Map'
    InteropInterface = 'InteropInterface'
    Any = 'Any'
    Void = 'Void'
