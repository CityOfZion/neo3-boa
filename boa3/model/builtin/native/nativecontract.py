from typing import List

from boa3.model.builtin.native.policyclass import PolicyClass
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.imports.package import Package


class NativeContract:

    Policy = PolicyClass()

    # region Packages

    PolicyModule = Package(identifier=Policy.identifier.lower(),
                           types=[Policy]
                           )

    # endregion

    package_symbols: List[IdentifiedSymbol] = [
        PolicyModule
    ]
