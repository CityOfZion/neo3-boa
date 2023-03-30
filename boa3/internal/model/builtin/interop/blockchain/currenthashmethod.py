from typing import Dict

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.nativecontract import LedgerMethod
from boa3.internal.model.variable import Variable


class CurrentHashMethod(LedgerMethod):
    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type
        identifier = '-get_current_hash'
        syscall = 'currentHash'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=UInt256Type.build())


class CurrentHashProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'current_hash'
        getter = CurrentHashMethod()
        super().__init__(identifier, getter)
