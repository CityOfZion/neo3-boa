from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.interop.runtime.triggertype import TriggerType
from boa3.model.variable import Variable


class TriggerMethod(InteropMethod):

    def __init__(self, trigger_type: TriggerType):
        identifier = 'trigger'
        syscall = 'System.Runtime.GetTrigger'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=trigger_type)
