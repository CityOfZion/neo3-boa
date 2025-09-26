from enum import Enum

from boa3.internal.model.builtin.builtin import Builtin
from boa3.internal.model.builtin.compile_time import NeoMetadataType
from boa3.internal.model.builtin.interop.contract.contractmanifest import *
from boa3.internal.model.builtin.interop.interop import Interop
from boa3.internal.model.builtin.native.nativecontract import NativeContract
from boa3.internal.model.imports.package import Package
from boa3.internal.model.type.math import Math


class BoaSCPackage(str, Enum):
    Contracts = 'contracts'
    Compiletime = 'compiletime'
    Math = 'math'
    Runtime = 'runtime'
    Storage = 'storage'
    Types = 'types'
    Utils = 'utils'


class ContractImports:

    @classmethod
    def package_symbols(cls, package: str = None) -> Package | None:
        if package in BoaSCPackage.__members__.values():
            return cls._pkg_tree[package]

    # region Contracts
    ContractManagementModule = Package(
        identifier=NativeContract.ContractManagement.identifier.lower(),
        types=[
            NativeContract.ContractManagement,
        ]
    )

    CryptoLibModule = Package(
        identifier=NativeContract.CryptoLib.identifier.lower(),
        types=[
            NativeContract.CryptoLib,
        ]
    )

    GasModule = Package(
        identifier=NativeContract.GAS.identifier.lower(),
        types=[
            NativeContract.GAS
        ]
    )

    LedgerModule = Package(
        identifier=NativeContract.Ledger.identifier.lower(),
        types=[
            NativeContract.Ledger
        ]
    )

    NeoModule = Package(
        identifier=NativeContract.NEO.identifier.lower(),
        types=[
            NativeContract.NEO
        ]
    )

    OracleModule = Package(
        identifier=NativeContract.Oracle.identifier.lower(),
        types=[
            NativeContract.Oracle
        ]
    )

    PolicyModule = Package(
        identifier=NativeContract.Policy.identifier.lower(),
        types=[
            NativeContract.Policy
        ]
    )

    RoleManagementModule = Package(
        identifier=NativeContract.RoleManagement.identifier.lower(),
        types=[
            NativeContract.RoleManagement,
        ]
    )

    StdLibModule = Package(
        identifier=NativeContract.StdLib.identifier.lower(),
        types=[
            NativeContract.StdLib
        ]
    )

    ContractsPackage = Package(
        identifier=BoaSCPackage.Contracts,
        types=[
            NativeContract.ContractManagement,
            NativeContract.CryptoLib,
            NativeContract.GAS,
            NativeContract.Ledger,
            NativeContract.NEO,
            NativeContract.Oracle,
            NativeContract.Policy,
            NativeContract.RoleManagement,
            NativeContract.StdLib,
        ],
        packages=[
            ContractManagementModule,
            CryptoLibModule,
            GasModule,
            LedgerModule,
            NeoModule,
            OracleModule,
            PolicyModule,
            RoleManagementModule,
            StdLibModule,
        ],
    )
    # endregion

    # region Compiletime
    CompiletimePackage = Package(
        identifier=BoaSCPackage.Compiletime,
        types=[
            NeoMetadataType,
        ],
        methods=[
            Builtin.Public,
            Builtin.ContractInterface,
            Builtin.ContractMethodDisplayName,
        ]
    )
    # endregion

    # region Math
    MathPackage = Package(
        identifier=BoaSCPackage.Math,
        methods=[
            Math.Sqrt,
            Builtin.BuiltinMathCeil,
            Builtin.BuiltinMathFloor,
        ],
    )
    # endregion

    # region Runtime
    RuntimePackage = Package(
        identifier=BoaSCPackage.Runtime,
        properties=[
            Interop.AddressVersion,
            Interop.BlockTime,
            Interop.CallingScriptHash,
            Interop.ExecutingScriptHash,
            Interop.GasLeft,
            Interop.Platform,
            Interop.InvocationCounter,
            Interop.EntryScriptHash,
            Interop.ScriptContainer,
            Interop.GetCurrentSigners
        ],
        methods=[
            Interop.BurnGas,
            Interop.CheckWitness,
            Interop.GetNetwork,
            Interop.GetNotifications,
            Interop.GetRandom,
            Interop.GetTrigger,
            Interop.LoadScript,
            Interop.Log,
            Interop.Notify
        ],
    )
    # endregion

    # region Storage
    StorageContextModule = Package(
        identifier=Interop.StorageContextType.identifier.lower(),
        types=[
            Interop.StorageContextType
        ]
    )

    StorageMapModule = Package(
        identifier=Interop.StorageMapType.identifier.lower(),
        types=[
            Interop.StorageMapType
        ]
    )

    StoragePackage = Package(
        identifier=BoaSCPackage.Storage,
        types=[
            Interop.StorageContextType,
            Interop.StorageMapType,
        ],
        methods=[
            Interop.StorageDelete,
            Interop.StorageFind,
            Interop.StorageGet,
            Interop.StorageGetInt,
            Interop.StorageGetBool,
            Interop.StorageGetStr,
            Interop.StorageGetList,
            Interop.StorageGetDict,
            Interop.StorageGetObject,
            Interop.StorageGetUInt160,
            Interop.StorageGetUInt256,
            Interop.StorageGetECPoint,
            Interop.StorageGetContext,
            Interop.StorageGetCheck,
            Interop.StorageGetCheckInt,
            Interop.StorageGetCheckBool,
            Interop.StorageGetCheckStr,
            Interop.StorageGetCheckList,
            Interop.StorageGetCheckDict,
            Interop.StorageGetCheckObject,
            Interop.StorageGetCheckUInt160,
            Interop.StorageGetCheckUInt256,
            Interop.StorageGetCheckECPoint,
            Interop.StorageGetReadOnlyContext,
            Interop.StoragePut,
            Interop.StoragePutInt,
            Interop.StoragePutBool,
            Interop.StoragePutStr,
            Interop.StoragePutList,
            Interop.StoragePutDict,
            Interop.StoragePutObject,
            Interop.StoragePutUInt160,
            Interop.StoragePutUInt256,
            Interop.StoragePutECPoint,
        ],
        packages=[
            StorageContextModule,
            StorageMapModule
        ]
    )
    # endregion

    # region Types
    TypesPackage = Package(
        identifier=BoaSCPackage.Types,
        types=[
            Builtin.UInt160,
            Builtin.UInt256,
            Builtin.ECPoint,
            Builtin.Event,
            Builtin.Address,
            Builtin.BlockHash,
            Builtin.PublicKey,
            Builtin.ScriptHashType_,
            Builtin.ScriptHashLittleEndian,
            Builtin.TransactionId,
            Interop.BlockType,
            Interop.SignerType,
            Interop.WitnessConditionType,
            Interop.WitnessCondition,
            Interop.WitnessRuleAction,
            Interop.WitnessRule,
            Interop.WitnessScope,
            Interop.TransactionType,
            Interop.ContractType,
            Interop.ContractManifestType,
            ContractAbiType.build(),
            ContractEventDescriptorType.build(),
            ContractGroupType.build(),
            ContractMethodDescriptorType.build(),
            ContractParameterDefinitionType.build(),
            ContractParameterTypeType.build(),
            ContractPermissionDescriptorType.build(),
            ContractPermissionType.build(),
            Builtin.Nep17Contract,
            Builtin.Opcode,
            Interop.FindOptionsType,
            Interop.NamedCurveHashType,
            Interop.Bls12381Type,
            Interop.RoleType,
            Interop.NotificationType,
            Interop.TriggerType,
            Interop.VMStateType,
            Interop.CallFlagsType,
            Interop.OracleResponseCode,
            Builtin.NeoAccountState,
            Interop.TransactionAttributeType,
        ],
    )
    # endregion

    # region Utils
    IteratorModule = Package(
        identifier=Interop.Iterator._identifier.lower(),
        types=[
            Interop.Iterator
        ]
    )

    UtilsPackage = Package(
        identifier=BoaSCPackage.Utils,
        methods=[
            Builtin.Env,
            Builtin.NewEvent,
            Builtin.Nep11Transfer,
            Builtin.Nep17Transfer,
            Builtin.ToHexStr,
            Builtin.ScriptHashMethod_,
            Interop.CallContract,
            Interop.GetCallFlags,
            Builtin.Abort,
            Interop.CheckSig,
            Interop.CheckMultisig,
            Interop.CreateStandardAccount,
            Interop.CreateMultisigAccount,
            Builtin.ConvertToBool,
            Builtin.ConvertIntToBytes,
            Builtin.ConvertStrToBytes,
            Builtin.ConvertToInt,
            Builtin.ConvertToStr,
            Interop.Hash160,
            Interop.Hash256,
        ],
        types=[
            Interop.Iterator
        ],
        packages=[
            IteratorModule
        ],
    )
    # endregion

    _pkg_tree: dict[BoaSCPackage, Package] = {
        pkg.identifier: pkg for pkg in [
            ContractsPackage,
            CompiletimePackage,
            MathPackage,
            RuntimePackage,
            StoragePackage,
            TypesPackage,
            UtilsPackage,
        ]
    }
