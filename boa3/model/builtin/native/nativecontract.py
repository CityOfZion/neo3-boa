from typing import List

from boa3.model.builtin.interop.interop import Interop
from boa3.model.builtin.native import *
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.imports.package import Package


class NativeContract:

    # Class Interfaces
    CryptoLib = CryptoLibClass()
    Ledger = LedgerClass()
    Policy = PolicyClass()
    RoleManagement = RoleManagementClass()
    StdLib = StdLibClass()

    # region Packages

    CryptoLibModule = Package(identifier=CryptoLib.identifier.lower(),
                              types=[CryptoLib])

    LedgerModule = Package(identifier=Ledger.identifier.lower(),
                           types=[Ledger,
                                  Interop.BlockType,
                                  Interop.TransactionType]
                           )

    PolicyModule = Package(identifier=Policy.identifier.lower(),
                           types=[Policy]
                           )

    RoleManagementModule = Package(identifier=RoleManagement.identifier.lower(),
                                   types=[RoleManagement,
                                          Interop.RoleType]
                                   )

    StdLibModule = Package(identifier=StdLib.identifier.lower(),
                           types=[StdLib]
                           )

    # endregion

    package_symbols: List[IdentifiedSymbol] = [
        CryptoLibModule,
        LedgerModule,
        PolicyModule,
        RoleManagementModule,
        StdLibModule
    ]
