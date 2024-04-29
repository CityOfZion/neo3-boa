from enum import Enum
from typing import Self


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

    @classmethod
    def union(cls, abi_types: list[Self]) -> Self:
        if len(abi_types) == 0:
            return AbiType.Any

        if len(abi_types) == 1:
            return abi_types[0]

        if AbiType.Void in abi_types:
            abi_types.remove(AbiType.Void)
            if len(abi_types) == 1:
                return abi_types[0]

        abis = abi_types[:1]
        for abi in abi_types[1:]:
            if abi not in abis:
                abis.append(abi)

        if len(abis) == 1:
            return abis[0]

        generic_mapping = {
            AbiType.Signature: AbiType.ByteArray,
            AbiType.Boolean: AbiType.Integer,
            AbiType.Integer: AbiType.Integer,
            AbiType.Hash160: AbiType.ByteArray,
            AbiType.Hash256: AbiType.ByteArray,
            AbiType.ByteArray: AbiType.ByteArray,
            AbiType.PublicKey: AbiType.ByteArray,
            AbiType.String: AbiType.ByteArray,
            AbiType.Array: AbiType.Array,
            AbiType.Map: AbiType.Map,
            AbiType.InteropInterface: AbiType.InteropInterface,
            AbiType.Any: AbiType.Any,
            AbiType.Void: AbiType.Void
        }

        generic_abis = [generic_mapping[abis[0]]]
        for abi in abis[1:]:
            generic = generic_mapping[abi]
            if generic not in generic_abis:
                generic_abis.append(generic)

        if len(generic_abis) == 1:
            return generic_abis[0]
        else:
            return AbiType.Any

    def __str__(self):
        return self.value
