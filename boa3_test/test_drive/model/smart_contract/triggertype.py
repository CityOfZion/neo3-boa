from __future__ import annotations

import enum


class TriggerType(enum.IntEnum):
    # Indicate that the contract is triggered by the system to execute the OnPersist method of the native contracts.
    OnPersist = 0x01

    # Indicate that the contract is triggered by the system to execute the PostPersist method of the native contracts.
    PostPersist = 0x02

    # Indicates that the contract is triggered by the verification of a IVerifiable.
    Verification = 0x20

    # Indicates that the contract is triggered by the execution of transactions.
    Application = 0x40

    # The combination of all system triggers.
    System = OnPersist | PostPersist

    # The combination of all triggers.
    All = OnPersist | PostPersist | Verification | Application

    def neo_name(self) -> str:
        return self.name

    @staticmethod
    def get_from_neo_name(neo_name: str) -> TriggerType:
        return TriggerType[neo_name]
