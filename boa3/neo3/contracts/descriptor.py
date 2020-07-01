from __future__ import annotations

import binascii

from boa3.neo3.core import IJson, types, cryptography


class ContractPermissionDescriptor(IJson):
    """
    A restriction object that limits the smart contract's calling abilities. Enforced at runtime.

    See Also: ContractManifest.
    """

    def __init__(self, contract_hash: types.UInt160 = None,
                 group: cryptography.EllipticCurve.ECPoint = None):
        """
        Create a contract hash or group based restriction. Mutually exclusive.
        Supply no arguments to create a wildcard permission descriptor.

        Raises:
            ValueError: if both contract hash and group arguments are supplied.
        """
        if contract_hash and group:
            raise ValueError("Maximum 1 argument can be supplied")
        self.contract_hash = contract_hash
        self.group = group

    def __eq__(self, other):
        return self.contract_hash == other.contract_hash and self.group == other.group

    @property
    def is_hash(self) -> bool:
        """
        Indicates if the permission is limited to a specific contract hash.
        """
        return self.contract_hash is not None

    @property
    def is_group(self) -> bool:
        """
        Indicates if the permission is limited to a specific group.
        """
        return self.group is not None

    @property
    def is_wildcard(self) -> bool:
        """
        Indicates if the permission is not limited to a specific contract or a specific group.
        """
        return not self.is_hash and not self.is_group

    def to_json(self) -> dict:
        """
        Convert object into JSON representation.
        """
        # NEO C# deviates here. They return a string
        if self.contract_hash:
            val = str(self.contract_hash)
        elif self.group:
            val = str(self.group)
        else:
            val = "*"
        return {'contract': val}

    @classmethod
    def from_json(cls, json: dict) -> ContractPermissionDescriptor:
        """
        Parse object out of JSON data.

        Args:
            json: a dictionary.

        Raises:
            KeyError: if the data supplied does not contain the necessary key.
            ValueError: if the data supplied cannot recreate a valid object.
        """
        # catches both missing key and None as value
        value = json.get('contract', None)
        if value is None:
            raise ValueError(f"Invalid JSON - Cannot deduce permission type from None")

        if len(value) == 40:
            return cls(contract_hash=types.UInt160.from_string(value))
        if len(value) == 66:
            ecpoint = cryptography.EllipticCurve.ECPoint.deserialize_from_bytes(binascii.unhexlify(value))
            return cls(group=ecpoint)
        if value == '*':
            return cls()  # no args == wildcard
        raise ValueError(f"Invalid JSON - Cannot deduce permission type from: {value}")
