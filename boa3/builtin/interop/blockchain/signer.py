from typing import List

from boa3.builtin.type import UInt160
from boa3.internal.neo3.network.payloads.verification import WitnessConditionType, WitnessRuleAction, WitnessScope


class Signer:
    """
    Represents a signer.

    :ivar account:
    :vartype account: UInt160
    :ivar scopes:
    :vartype scopes: WitnessScope
    :ivar allowed_contracts:
    :vartype allowed_contracts: List[UInt160]
    :ivar allowed_groups:
    :vartype allowed_groups: List[UInt160]
    :ivar rules:
    :vartype rules: List[WitnessRule]
    """

    def __init__(self):
        self.account: UInt160 = UInt160()
        self.scopes: WitnessScope = WitnessScope.NONE
        self.allowed_contracts: List[UInt160] = []
        self.allowed_groups: List[UInt160] = []
        self.rules: List[WitnessRule] = []


class WitnessRule:
    """
    Represents a witness rule.

    :ivar action:
    :vartype action: WitnessRuleAction
    :ivar condition:
    :vartype condition: WitnessCondition
    """

    def __init__(self):
        self.action: WitnessRuleAction = WitnessRuleAction.DENY
        self.condition: WitnessCondition = WitnessCondition()


class WitnessCondition:
    """
    Represents a witness condition.

    :ivar type:
    :vartype type: WitnessConditionType
    """

    def __init__(self):
        self.type: WitnessConditionType = WitnessConditionType.BOOLEAN
