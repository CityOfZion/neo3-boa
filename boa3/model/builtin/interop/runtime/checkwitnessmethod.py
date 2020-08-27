from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class CheckWitnessMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'check_witness'
        syscall = 'System.Runtime.CheckWitness'
        args: Dict[str, Variable] = {'hash_or_pubkey': Variable(Type.bytes)}
        super().__init__(identifier, syscall, args, return_type=Type.bool)
