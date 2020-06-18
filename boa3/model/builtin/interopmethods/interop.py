from typing import List

from boa3.model.builtin.interopmethods.checkwitnessmethod import CheckWitnessMethod
from boa3.model.builtin.interopmethods.interopmethod import InteropMethod


class Interop:

    @classmethod
    def interop_methods(cls) -> List[InteropMethod]:
        return [interop for interop in vars(cls).values() if isinstance(interop, InteropMethod)]

    CheckWitness = CheckWitnessMethod()
