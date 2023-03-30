from typing import Dict

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.runtime.triggertype import TriggerType
from boa3.internal.model.variable import Variable


class GetTriggerMethod(InteropMethod):

    def __init__(self, trigger_type: TriggerType):
        identifier = 'get_trigger'
        syscall = 'System.Runtime.GetTrigger'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=trigger_type)
