import enum
from typing import Self


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

    @classmethod
    def get_from_neo_name(cls, neo_name: str) -> Self:
        return TriggerType[neo_name]
