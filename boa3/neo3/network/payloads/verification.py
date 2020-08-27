from __future__ import annotations

import hashlib
from enum import IntFlag
from typing import List

from boa3.neo3.core import serialization, utils, types, cryptography, Size as s
from boa3.neo3.network import payloads


class Cosigner(serialization.ISerializable):
    """
    A class that specifies who can pass CheckWitness() verifications in a smart contract.
    """

    def __init__(self, account: types.UInt160 = None,
                 scope: payloads.WitnessScope = None,
                 allowed_contracts: List[types.UInt160] = None,
                 allowed_groups: List[cryptography.EllipticCurve.ECPoint] = None):
        #: The TX sender.
        self.account = account if account else types.UInt160.zero()
        #: payloads.WitnessScope: The configured validation scope.
        self.scope = scope if scope else payloads.WitnessScope.GLOBAL
        #: List[types.UInt160]: Whitelist of contract hashes if used with
        #: :const:`~neo3.network.payloads.verification.WitnessScope.CUSTOM_CONTRACTS`.
        self.allowed_contracts = allowed_contracts if allowed_contracts else []
        #: List[cryptography.EllipticCurve.ECPoint]: Whitelist of public keys if used with
        #: :const:`~neo3.network.payloads.verification.WitnessScope.CUSTOM_GROUPS`.
        self.allowed_groups = allowed_groups if allowed_groups else []

    def __len__(self):
        contracts_size = 0
        if payloads.WitnessScope.CUSTOM_CONTRACTS in self.scope:
            contracts_size = utils.get_var_size(self.allowed_contracts)

        groups_size = 0
        if payloads.WitnessScope.CUSTOM_GROUPS in self.scope:
            groups_size = utils.get_var_size(self.allowed_groups)

        return s.uint160 + s.uint8 + contracts_size + groups_size

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_serializable(self.account)
        writer.write_uint8(self.scope)

        if payloads.WitnessScope.CUSTOM_CONTRACTS in self.scope:
            writer.write_serializable_list(self.allowed_contracts)

        if payloads.WitnessScope.CUSTOM_GROUPS in self.scope:
            writer.write_serializable_list(self.allowed_groups)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.account = reader.read_serializable(types.UInt160)
        self.scope = payloads.WitnessScope(reader.read_uint8())

        if payloads.WitnessScope.CUSTOM_CONTRACTS in self.scope:
            self.allowed_contracts = reader.read_serializable_list(types.UInt160)

        if payloads.WitnessScope.CUSTOM_GROUPS in self.scope:
            self.allowed_groups = reader.read_serializable_list(cryptography.EllipticCurve.ECPoint)


class Witness(serialization.ISerializable):
    """
    An executable verification script that validates a verifiable object like a transaction.
    """

    def __init__(self, invocation_script: bytes = None, verification_script: bytes = None):
        #: A set of VM instructions to setup the stack for verification.
        self.invocation_script = invocation_script if invocation_script else b''
        #: A set of VM instructions that does the actual verification.
        #: It is expected to set the result stack to a boolean True if validation passed.
        self.verification_script = verification_script if verification_script else b''
        self._script_hash = None

    def __len__(self):
        return utils.get_var_size(self.invocation_script) + utils.get_var_size(self.verification_script)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_var_bytes(self.invocation_script)
        writer.write_var_bytes(self.verification_script)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.invocation_script = reader.read_var_bytes(max=664)
        self.verification_script = reader.read_var_bytes(max=360)

    def script_hash(self) -> types.UInt160:
        """ Get the script hash based on the verification script."""
        intermediate_data = hashlib.sha256(self.verification_script).digest()
        data = hashlib.new('ripemd160', intermediate_data).digest()
        return types.UInt160(data=data)


class WitnessScope(IntFlag):
    """
    Determine the rules for a smart contract :func:`CheckWitness()` sys call.
    """
    #: Allow the witness in all context. Equal to NEO 2.x's default behaviour.
    GLOBAL = 0x00
    #: Allow the witness if the current calling script hash equals the entry script hash into the virtual machine.
    #: Using this prevents passing :func:`CheckWitness()` in a smart contract called via another smart contract.
    CALLED_BY_ENTRY = 0x01
    #: Allow the witness if called from a smart contract that is whitelisted in the cosigner
    #: :attr:`~neo3.network.payloads.verification.Cosigner.allowed_contracts` attribute.
    CUSTOM_CONTRACTS = 0x10
    #: Allow the witness if it any public key in the cosigner
    #: :attr:`~neo3.network.payloads.verification.Cosigner.allowed_groups` attribute is whitelisted in the contracts
    #: manifest.groups array.
    CUSTOM_GROUPS = 0x20
