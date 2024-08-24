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

    # Deprecated Native Contract Names
    gas_name = 'GAS'
    ledger_name = 'Ledger'
    neo_name = 'NEO'
    oracle_name = 'Oracle'
    policy_name = 'Policy'

    # region Packages

    ContractManagementModule = Package(deprecated=True,
                                       new_location='boa3.sc.contracts',

                                       identifier=ContractManagement.identifier.lower(),
                                       types=[ContractManagement,
                                              Interop.ContractType])

    CryptoLibModule = Package(deprecated=True,
                              new_location='boa3.sc.contracts',
                              identifier=CryptoLib.identifier.lower(),
                              types=[CryptoLib,
                                     Interop.NamedCurveHashType,
                                     Interop.Bls12381Type])

    GasModule = Package(deprecated=True,
                        new_location='boa3.sc.contracts',
                        identifier=gas_name.lower(),
                        other_symbols={
                            gas_name: GAS
                        }
                        )

    LedgerModule = Package(deprecated=True,
                           new_location='boa3.sc.contracts',
                           identifier=ledger_name.lower(),
                           other_symbols={
                               ledger_name: Ledger
                           }
                           )

    NeoModule = Package(deprecated=True,
                        new_location='boa3.sc.contracts',
                        identifier=neo_name.lower(),
                        other_symbols={
                            neo_name: NEO
                        }
                        )

    OracleModule = Package(deprecated=True,
                           new_location='boa3.sc.contracts',
                           identifier=oracle_name.lower(),
                           other_symbols={
                               oracle_name: Oracle
                           }
                           )

    PolicyModule = Package(deprecated=True,
                           new_location='boa3.sc.contracts',
                           identifier=policy_name.lower(),
                           other_symbols={
                               policy_name: Policy
                           }
                           )

    RoleManagementModule = Package(deprecated=True,
                                   new_location='boa3.sc.contracts',
                                   identifier=RoleManagement.identifier.lower(),
                                   types=[RoleManagement,
                                          Interop.RoleType]
                                   )

    StdLibModule = Package(deprecated=True,
                           new_location='boa3.sc.contracts',
                           identifier=StdLib.identifier.lower(),
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
