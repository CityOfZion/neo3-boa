__all__ = [
    "Signer",
    "WitnessRule",
    "WitnessCondition",
    "WitnessConditionType",
    "WitnessRuleAction",
    "WitnessScope",
]

from boa3.builtin.type import UInt160
from boa3.internal.deprecation import deprecated
from boa3.internal.neo3.network.payloads.verification import WitnessConditionType, WitnessRuleAction, WitnessScope


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.types` instead')
class Signer:
    """
    Represents a signer.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Transactions#signers>`__ to learn more
    about Signers.

    :ivar account:
    :vartype account: boa3.builtin.type.UInt160
    :ivar scopes:
    :vartype scopes: WitnessScope
    :ivar allowed_contracts:
    :vartype allowed_contracts: list[boa3.builtin.type.UInt160]
    :ivar allowed_groups:
    :vartype allowed_groups: list[boa3.builtin.type.UInt160]
    :ivar rules:
    :vartype rules: list[WitnessRule]
    """

    def __init__(self):
        self.account: UInt160 = UInt160()
        self.scopes: WitnessScope = WitnessScope.NONE
        self.allowed_contracts: list[UInt160] = []
        self.allowed_groups: list[UInt160] = []
        self.rules: list[WitnessRule] = []


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.types` instead')
class WitnessRule:
    """
    Represents a witness rule.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Transactions#witnessrule>`__ to learn
    more about WitnessRules.

    :ivar action:
    :vartype action: WitnessRuleAction
    :ivar condition:
    :vartype condition: WitnessCondition
    """

    def __init__(self):
        self.action: WitnessRuleAction = WitnessRuleAction.DENY
        self.condition: WitnessCondition = WitnessCondition()


@deprecated(details='This module is deprecated. Use :mod:`boa3.sc.types` instead')
class WitnessCondition:
    """
    Represents a witness condition.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Transactions#witnesscondition>`__ to
    learn more about WitnessConditions.

    :ivar type:
    :vartype type: WitnessConditionType
    """

    def __init__(self):
        self.type: WitnessConditionType = WitnessConditionType.BOOLEAN
