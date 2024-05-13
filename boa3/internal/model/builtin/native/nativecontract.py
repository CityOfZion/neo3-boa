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

    GAS_ = GAS.clone()
    GAS_._identifier = gas_name
    Ledger_ = Ledger.clone()
    Ledger_._identifier = ledger_name
    NEO_ = NEO.clone()
    NEO_._identifier = neo_name
    Oracle_ = Oracle.clone()
    Oracle_._identifier = oracle_name
    Policy_ = Policy.clone()
    Policy_._identifier = policy_name

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
                                     Interop.NamedCurveType,
                                     Interop.Bls12381Type])

    GasModule = Package(deprecated=True,
                        new_location='boa3.sc.contracts',
                        identifier=gas_name.lower(),
                        types=[GAS_]
                        )

    LedgerModule = Package(deprecated=True,
                           new_location='boa3.sc.contracts',
                           identifier=ledger_name.lower(),
                           types=[Ledger_]
                           )

    NeoModule = Package(deprecated=True,
                        new_location='boa3.sc.contracts',
                        identifier=neo_name.lower(),
                        types=[NEO_]
                        )

    OracleModule = Package(deprecated=True,
                           new_location='boa3.sc.contracts',
                           identifier=oracle_name.lower(),
                           types=[Oracle_]
                           )

    PolicyModule = Package(deprecated=True,
                           new_location='boa3.sc.contracts',
                           identifier=policy_name.lower(),
                           types=[Policy_]
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
