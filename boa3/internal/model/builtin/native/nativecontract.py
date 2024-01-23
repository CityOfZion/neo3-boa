from boa3.internal.model.builtin.interop.interop import Interop
from boa3.internal.model.builtin.native import *
from boa3.internal.model.builtin.native.oracleclass import OracleClass
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.imports.package import Package


class NativeContract:
    # Class Interfaces
    ContractManagement = ContractManagementClass.build()
    CryptoLib = CryptoLibClass.build()
    GAS = GasClass.build()
    Ledger = LedgerClass.build()
    NEO = NeoClass.build()
    Oracle = OracleClass.build()
    Policy = PolicyClass.build()
    RoleManagement = RoleManagementClass.build()
    StdLib = StdLibClass.build()

    # region Packages

    ContractManagementModule = Package(identifier=ContractManagement.identifier.lower(),
                                       types=[ContractManagement,
                                              Interop.ContractType])

    CryptoLibModule = Package(identifier=CryptoLib.identifier.lower(),
                              types=[CryptoLib,
                                     Interop.NamedCurveType,
                                     Interop.Bls12381Type])

    GasModule = Package(identifier=GAS.identifier.lower(),
                        types=[GAS]
                        )

    LedgerModule = Package(identifier=Ledger.identifier.lower(),
                           types=[Ledger]
                           )

    NeoModule = Package(identifier=NEO.identifier.lower(),
                        types=[NEO]
                        )

    OracleModule = Package(identifier=Oracle.identifier.lower(),
                           types=[Oracle]
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

    package_symbols: list[IdentifiedSymbol] = [
        ContractManagementModule,
        CryptoLibModule,
        GasModule,
        LedgerModule,
        NeoModule,
        OracleModule,
        PolicyModule,
        RoleManagementModule,
        StdLibModule
    ]
