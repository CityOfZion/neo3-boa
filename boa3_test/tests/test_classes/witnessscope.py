from __future__ import annotations

import enum


class WitnessScope(enum.IntEnum):
    # Indicates that no contract was witnessed. Only sign the transaction.
    _None = 0

    # Indicates that the calling contract must be the entry contract. The witness/permission/signature
    # given on first invocation will automatically expire if entering deeper internal
    # invokes. This can be the default safe choice for native NEO/GAS (previously used
    # on Neo 2 as "attach" mode).
    CalledByEntry = 1

    # Custom hash for contract-specific.
    CustomContracts = 16

    # Custom pubkey for group members.
    CustomGroups = 32

    # Indicates that the current context must satisfy the specified rules.
    WitnessRules = 64

    # This allows the witness in all contexts (default Neo2 behavior).
    Global = 128

    def neo_name(self) -> str:
        if self is WitnessScope._None:
            return 'None'
        else:
            return self.name

    @staticmethod
    def get_from_neo_name(neo_name: str) -> WitnessScope:
        if neo_name == 'None':
            return WitnessScope._None
        elif neo_name != WitnessScope._None.name:
            return WitnessScope[neo_name]
