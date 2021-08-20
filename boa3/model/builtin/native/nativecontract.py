from typing import List

from boa3.model.builtin.interop.blockchain import BlockType, TransactionType
from boa3.model.builtin.interop.role import RoleType
from boa3.model.builtin.native import *
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.imports.package import Package


class NativeContract:

    # Interop Types
    BlockType = BlockType.build()
    RoleType = RoleType()
    TransactionType = TransactionType.build()

    # Class Interfaces
    CryptoLib = CryptoLibClass()
    Ledger = LedgerClass()
    Policy = PolicyClass()
    Role = RoleManagementClass()

    # region Packages

    CryptoLibModule = Package(identifier=CryptoLib.identifier.lower(),
                              types=[CryptoLib])

    LedgerModule = Package(identifier=Ledger.identifier.lower(),
                           types=[Ledger,
                                  BlockType,
                                  TransactionType]
                           )

    PolicyModule = Package(identifier=Policy.identifier.lower(),
                           types=[Policy]
                           )

    RoleModule = Package(identifier=Role.identifier.lower(),
                         types=[Role,
                                RoleType]
                         )

    # endregion

    package_symbols: List[IdentifiedSymbol] = [
        CryptoLibModule,
        LedgerModule,
        PolicyModule,
        RoleModule,
    ]
