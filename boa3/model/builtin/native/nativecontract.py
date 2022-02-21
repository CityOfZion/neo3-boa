from typing import List

from boa3.model.builtin.builtin import Builtin
from boa3.model.builtin.interop.interop import Interop
from boa3.model.builtin.native import *
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.imports.package import Package


class NativeContract:
    # Class Interfaces
    ContractManagement = ContractManagementClass()
    CryptoLib = CryptoLibClass()
    GAS = GasClass()
    Ledger = LedgerClass()
    NEO = NeoClass()
    Policy = PolicyClass()
    RoleManagement = RoleManagementClass()
    StdLib = StdLibClass()

    # region Packages

    ContractManagementModule = Package(identifier=ContractManagement.identifier.lower(),
                                       types=[ContractManagement,
                                              Interop.ContractType,
                                              Builtin.UInt160])

    CryptoLibModule = Package(identifier=CryptoLib.identifier.lower(),
                              types=[CryptoLib,
                                     Interop.NamedCurveType])

    GasModule = Package(identifier=GAS.identifier.lower(),
                        types=[GAS]
                        )

    LedgerModule = Package(identifier=Ledger.identifier.lower(),
                           types=[Ledger,
                                  Interop.BlockType,
                                  Interop.TransactionType]
                           )

    NeoModule = Package(identifier=NEO.identifier.lower(),
                        types=[NEO]
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
        ContractManagementModule,
        CryptoLibModule,
        GasModule,
        LedgerModule,
        NeoModule,
        PolicyModule,
        RoleManagementModule,
        StdLibModule
    ]
