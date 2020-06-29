from __future__ import annotations

import base64
import binascii
import json
from enum import IntFlag
from typing import List, Callable

from boa3.neo3 import contracts
from boa3.neo3.core import serialization, types, IJson, cryptography, utils
from boa3.neo3.core.serialization import BinaryReader, BinaryWriter


class ContractGroup(IJson):
    """
    Describes a set of mutually trusted contracts.

    See Also: ContractManifest.
    """

    def __init__(self, public_key: cryptography.EllipticCurve.ECPoint, signature: bytes):
        self.public_key = public_key
        self.signature = signature

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.public_key == other.public_key and self.signature == other.signature

    def is_valid(self, contract_hash: types.UInt160) -> bool:
        """
        Validate if the group has agreed on allowing the specific contract_hash.

        Args:
            contract_hash:
        """
        return cryptography.verify_signature(contract_hash.to_array(),
                                             self.signature,
                                             self.public_key.encode_point(False))

    def to_json(self) -> dict:
        """
        Convert object into JSON representation.
        """
        json = {
            'pubKey': str(self.public_key),
            'signature': base64.b64encode(self.signature).decode()
        }
        return json

    @classmethod
    def from_json(cls, json: dict) -> ContractGroup:
        """
        Parse object out of JSON data.

        Args:
            json: a dictionary.

        Raises:
            KeyError: if the data supplied does not contain the necessary keys.
        """
        return cls(
            public_key=cryptography.EllipticCurve.ECPoint.deserialize_from_bytes(binascii.unhexlify(json['pubKey'])),
            signature=base64.b64decode(json['signature'].encode('utf8'))
        )


class ContractPermission(IJson):
    """
    An object describing a single set of outgoing call restrictions for a 'System.Contract.Call' SYSCALL.
    It describes what other smart contracts the executing contract is allowed to call and what exact methods on the
    other contract are allowed to be called. This is enforced during runtime.

    Example:
        Contract A (the executing contract) wants to call method "x" on Contract B. The runtime will query the manifest
        of Contract A and ask if this is allowed. The Manifest will search through its permissions (a list of
        ContractPermission objects) and ask if this "is_allowed(target_contract, target_method)".
    """

    def __init__(self, contract: contracts.ContractPermissionDescriptor, methods: WildcardContainer):
        self.contract = contract
        self.methods = methods

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.contract == other.contract and self.methods == other.methods

    @classmethod
    def default_permissions(cls) -> ContractPermission:
        """
        Construct a ContractPermission which allows any contract and any method to be called.
        """
        return cls(contracts.ContractPermissionDescriptor(),  # with no parameters equals to Wildcard
                   WildcardContainer.create_wildcard())

    def is_allowed(self, manifest: ContractManifest, method: str) -> bool:
        """
        Return if it is allowed to call `method` on contract `manifest.contract_hash`.

        Args:
            manifest: the manifest of the contract to be called.
            method: the method of the contract to be called.
        """
        if self.contract.is_hash:
            if not self.contract.contract_hash == manifest.contract_hash:
                return False
        elif self.contract.is_group:
            results = list(map(lambda p: p.public_key != self.contract.group, manifest.groups))
            if all(results):
                return False
        return self.methods.is_wildcard or method in self.methods

    def to_json(self) -> dict:
        """
        Convert object into JSON representation.
        """
        json = self.contract.to_json()
        # because NEO C# returns a string from "method" instead of sticking to a standard interface
        json.update({'methods': self.methods.to_json()['wildcard']})
        return json

    @classmethod
    def from_json(cls, json: dict) -> ContractPermission:
        """
        Parse object out of JSON data.

        Args:
            json: a dictionary.

        Raises:
            KeyError: if the data supplied does not contain the necessary keys.
        """
        cpd = contracts.ContractPermissionDescriptor.from_json(json)
        json_wildcard = {'wildcard': json['methods']}
        methods = WildcardContainer.from_json(json_wildcard)
        return cls(cpd, methods)


class ContractFeatures(IntFlag):
    NO_PROPERTY = 0,
    #: Indicate the contract has storage.
    HAS_STORAGE = 1 << 0
    #: Indicate the contract accepts tranfers.
    PAYABLE = 1 << 2


class WildcardContainer(IJson):
    """
    An internal helper class for ContractManifest attributes.
    """

    def __init__(self, data: list = None):
        self._is_wildcard = False
        self._data = data if data else []

    def __contains__(self, item):
        return item in self._data

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self._data == other._data

    @classmethod
    def create_wildcard(cls) -> WildcardContainer:
        """
        Creates an instance that indicates any value is allowed.
        """
        instance = cls()
        instance._is_wildcard = True
        return instance

    @property
    def is_wildcard(self) -> bool:
        """
        Indicates if the container is configured to allow all values.
        """
        return self._is_wildcard

    def to_json(self) -> dict:
        """
        Convert object into JSON representation.
        """
        if self.is_wildcard:
            return {'wildcard': '*'}
        return {'wildcard': list(map(lambda d: str(d), self._data))}

    @classmethod
    def from_json(cls, json: dict):
        """
        Parse object out of JSON data.

        Note: if the value is not '*', and is a Python list, then it will assume
        that the list members are strings or convertible via str().

        If the wildcard should contain other data types, use the alternative `from_json_as_type()` method

        Args:
            json: a dictionary.

        Raises:
            KeyError: if the data supplied does not contain the necessary key.
            ValueError: if the data supplied cannot recreate a valid object.
        """
        value = json.get('wildcard', None)
        if value is None:
            raise ValueError(f"Invalid JSON - Cannot recreate wildcard from None")
        if value == '*':
            return WildcardContainer.create_wildcard()
        if isinstance(value, list):
            return WildcardContainer(data=list(map(lambda d: str(d), value)))
        raise ValueError(f"Invalid JSON - Cannot deduce WildcardContainer type from: {value}")

    @classmethod
    def from_json_as_type(cls, json: dict, conversion_func: Callable):
        """
            Parse object out of JSON data.

            Note: if the value is not '*', and is a Python list, then it will use `conversion_func` to
            parse the members into the expected types.

        Args:
            json: a dictionary.
            conversion_func: a callable that takes 1 argument, which is the element in the value list

            Example with UInt160:
                {'wildcard': ['0xa400ff00ff00ff00ff00ff00ff00ff00ff00ff01', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']}

                 the first call has as argument '0xa400ff00ff00ff00ff00ff00ff00ff00ff00ff01'.
                 to process this example call
                 WildcardContainer.from_json_as_type(json_data, lambda f: types.UInt160.from_string(f))

        Raises:
            KeyError: if the data supplied does not contain the necessary key.
            ValueError: if the data supplied cannot recreate a valid object.
        """
        value = json.get('wildcard', None)
        if value is None:
            raise ValueError(f"Invalid JSON - Cannot recreate wildcard from None")
        if value == '*':
            return WildcardContainer.create_wildcard()
        if isinstance(value, list):
            return WildcardContainer(data=list(map(lambda d: conversion_func(d), value)))
        raise ValueError(f"Invalid JSON - Cannot deduce WildcardContainer type from: {value}")


class ContractManifest(serialization.ISerializable, IJson):
    """
    A description of a smart contract's abilities (callable methods & events) as well as a set of restrictions
    describing what external contracts and methods are allowed to be called.

    For more information see:
    https://github.com/neo-project/proposals/blob/3e492ad05d9de97abb6524fb9a73714e2cdc5461/nep-15.mediawiki
    """
    #: The maximum byte size after serialization to be considered valid a valid contract.
    MAX_LENGTH = 2048

    def __init__(self, contract_hash: types.UInt160 = types.UInt160.zero()):
        """
        Creates a default contract manifest if not arguments are supplied.

        A default contract is not Payable and has no storage as configured by its features.
        It may not be called by any other contracts

        Args:
            contract_hash: the contract script hash to create a manifest for.
        """
        #: A group represents a set of mutually trusted contracts. A contract will trust and allow any contract in the
        #: same group to invoke it.
        self.groups: List[ContractGroup] = []

        #: Features describe what contract abilities are available. TODO: link to contract features
        self.features: ContractFeatures = ContractFeatures.NO_PROPERTY

        #: For technical details of ABI, please refer to NEP-14: NeoContract ABI.
        #: https://github.com/neo-project/proposals/blob/d1f4e9e1a67d22a5755c45595121f80b0971ea64/nep-14.mediawiki
        self.abi: contracts.ContractABI = contracts.ContractABI(
            contract_hash=contract_hash,
            entry_point=contracts.ContractMethodDescriptor.default_entrypoint(),
            events=[],
            methods=[]
        )

        #: Permissions describe what external contract(s) and what method(s) on these are allowed to be invoked.
        self.permissions: List[contracts.ContractPermission] = [contracts.ContractPermission.default_permissions()]

        self.contract_hash: types.UInt160 = self.abi.contract_hash

        # Update trusts/safe_methods with outcome of https://github.com/neo-project/neo/issues/1664
        # Unfortunately we have to add this nonsense logic or we get deviating VM results.
        self.trusts = WildcardContainer()  # for UInt160 types
        self.safe_methods = WildcardContainer()  # for string types
        self.extra = None

    def __len__(self):
        return utils.get_var_size(str(self.to_json()).replace(' ', ''))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.groups == other.groups
                and self.features == other.features
                and self.abi == other.abi
                and self.permissions == other.permissions
                and self.trusts == other.trusts
                and self.safe_methods == other.safe_methods
                and self.extra == other.extra)

    def serialize(self, writer: BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_var_string(json.dumps(self.to_json()).replace(' ', ''))

    def deserialize(self, reader: BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self._deserialize_from_json(json.loads(reader.read_var_string(self.MAX_LENGTH)))

    def _deserialize_from_json(self, json: dict) -> None:
        self.abi = contracts.ContractABI.from_json(json['abi'])
        self.groups = list(map(lambda g: ContractGroup.from_json(g), json['groups']))
        self.features = ContractFeatures.NO_PROPERTY
        if json['features']['storage']:
            self.features |= ContractFeatures.HAS_STORAGE
        if json['features']['payable']:
            self.features |= ContractFeatures.PAYABLE
        self.permissions = list(map(lambda p: ContractPermission.from_json(p), json['permissions']))

        self.trusts = WildcardContainer.from_json_as_type(
            {'wildcard': json['trusts']},
            lambda t: types.UInt160.from_string(t))

        # converting json key/value back to default WildcardContainer format
        self.safe_methods = WildcardContainer.from_json({'wildcard': json['safeMethods']})
        self.extra = json['extra']

    def to_json(self) -> dict:
        """
        Convert object into JSON representation.
        """
        trusts = list(map(lambda m: "0x" + m, self.trusts.to_json()['wildcard']))
        json = {
            "groups": list(map(lambda g: g.to_json(), self.groups)),
            "features": {
                "storage": contracts.ContractFeatures.HAS_STORAGE in self.features,
                "payable": contracts.ContractFeatures.PAYABLE in self.features,
            },
            "abi": self.abi.to_json(),
            "permissions": list(map(lambda p: p.to_json(), self.permissions)),
            "trusts": trusts,
            "safeMethods": self.safe_methods.to_json()['wildcard'],
            "extra": self.extra
        }
        return json

    @classmethod
    def from_json(cls, json: dict):
        """
        Parse object out of JSON data.

        Args:
            json: a dictionary.

        Raise:
            KeyError: if the data supplied does not contain the necessary keys.
        """
        instance = cls(types.UInt160.zero())
        instance._deserialize_from_json(json)
        return instance

    def is_valid(self, contract_hash: types.UInt160) -> bool:
        """
        Test the manifest data for correctness and return the result.

        - Compares the manifest ABI with the `contract_hash`
        - Validates the manifest groups with the `contract_hash`

        An example use-case is to create and update smart contracts in a safe manner on the chain.

        Args:
            contract_hash:

        """
        if not self.abi.contract_hash == contract_hash:
            return False
        result = list(map(lambda g: g.is_valid(contract_hash), self.groups))
        return all(result)

    def can_call(self, target_manifest: ContractManifest, method: str) -> bool:
        """
        Convenience function to check if it is allowed to call `method` on `target_manifest` from this contract.

        Args:
            target_manifest: The manifest describing the target contract.
            method: the name of the target method.
        """
        results = list(map(lambda p: p.is_allowed(target_manifest, method), self.permissions))
        return any(results)
