from enum import IntEnum, IntFlag


class WitnessScope(IntFlag):
    """
    Determine the rules for a smart contract :func:`CheckWitness()` sys call.
    """
    #: No Contract was witnessed. Only sign the transaction.
    NONE = 0x0
    #: Allow the witness if the current calling script hash equals the entry script hash into the virtual machine.
    #: Using this prevents passing :func:`CheckWitness()` in a smart contract called via another smart contract.
    CALLED_BY_ENTRY = 0x01
    #: Allow the witness if called from a smart contract that is whitelisted in the signer
    #: :attr:`~neo3.network.payloads.verification.Signer.allowed_contracts` attribute.
    CUSTOM_CONTRACTS = 0x10
    #: Allow the witness if any public key is in the signer
    #: :attr:`~neo3.network.payloads.verification.Signer.allowed_groups` attribute is whitelisted in the contracts
    #: manifest.groups array.
    CUSTOM_GROUPS = 0x20
    #: Allow the witness if the specified :attr:`~neo3.network.payloads.verification.Signer.rules` are satisfied
    WITNESS_RULES = 0x40
    #: Allow the witness in all context. Equal to NEO 2.x's default behaviour.
    GLOBAL = 0x80

    def to_csharp_name(self) -> str:
        """
        Internal helper to match C# convention
        """
        if self == 0:
            return "None"
        flags = []
        if self.CALLED_BY_ENTRY in self:
            flags.append("CalledByEntry")
        if self.CUSTOM_CONTRACTS in self:
            flags.append("CustomContracts")
        if self.CUSTOM_GROUPS in self:
            flags.append("CustomGroups")
        if self.WITNESS_RULES in self:
            flags.append("WitnessRules")
        if self.GLOBAL in self:
            flags.append("Global")
        return ", ".join(flags)

    @classmethod
    def from_chsarp_name(cls, csharp_name):
        """
        Internal helper to parse from C# convention
        """
        c = cls(cls.NONE)
        if "CalledByEntry" in csharp_name:
            c |= c.CALLED_BY_ENTRY
        if "CustomContracts" in csharp_name:
            c |= c.CUSTOM_CONTRACTS
        if "CustomGroups" in csharp_name:
            c |= c.CUSTOM_GROUPS
        if "WitnessRules" in csharp_name:
            c |= c.WITNESS_RULES
        if "Global" in csharp_name:
            c |= c.GLOBAL
        return c


class WitnessRuleAction(IntEnum):
    DENY = 0
    ALLOW = 1


class WitnessConditionType(IntEnum):
    BOOLEAN = 0x0
    NOT = 0x01
    AND = 0x2
    OR = 0x03
    SCRIPT_HASH = 0x18
    GROUP = 0x19
    CALLED_BY_ENTRY = 0x20
    CALLED_BY_CONTRACT = 0x28
    CALLED_BY_GROUP = 0x29

    def to_csharp_string(self) -> str:
        if self == WitnessConditionType.SCRIPT_HASH:
            return "ScriptHash"
        elif self == WitnessConditionType.CALLED_BY_ENTRY:
            return "CalledByEntry"
        elif self == WitnessConditionType.CALLED_BY_CONTRACT:
            return "CalledByContract"
        elif self == WitnessConditionType.CALLED_BY_GROUP:
            return "CalledByGroup"
        else:
            return self.name.title()
