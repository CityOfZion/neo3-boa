from enum import Enum

from boa3.internal.model.builtin.interop.blockchain import *
from boa3.internal.model.builtin.interop.contract import *
from boa3.internal.model.builtin.interop.contract.contractmanifest import *
from boa3.internal.model.builtin.interop.crypto import *
from boa3.internal.model.builtin.interop.iterator import *
from boa3.internal.model.builtin.interop.json import *
from boa3.internal.model.builtin.interop.nativecontract import *
from boa3.internal.model.builtin.interop.oracle import *
from boa3.internal.model.builtin.interop.policy import *
from boa3.internal.model.builtin.interop.role import *
from boa3.internal.model.builtin.interop.runtime import *
from boa3.internal.model.builtin.interop.stdlib import *
from boa3.internal.model.builtin.interop.storage import *
from boa3.internal.model.event import Event
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.imports.package import Package

__all__ = ['Interop',
           'InteropPackage'
           ]


class InteropPackage(str, Enum):
    Blockchain = 'blockchain'
    Contract = 'contract'
    Crypto = 'crypto'
    Iterator = 'iterator'
    Json = 'json'
    Oracle = 'oracle'
    Policy = 'policy'
    Role = 'role'
    Runtime = 'runtime'
    Stdlib = 'stdlib'
    Storage = 'storage'


class Interop:
    @classmethod
    def get_symbol(cls, symbol_id: str) -> IdentifiedSymbol | None:
        for pkg_symbols in cls._interop_symbols.values():
            for method in pkg_symbols:
                if method.identifier == symbol_id:
                    return method

    @classmethod
    def interop_symbols(cls, package: str = None) -> list[IdentifiedSymbol]:
        if package in InteropPackage.__members__.values():
            return cls._interop_symbols[package]

        lst: list[IdentifiedSymbol] = []
        for symbols in cls._interop_symbols.values():
            lst.extend(symbols)
        return lst

    @classmethod
    def interop_events(cls) -> list[Event]:
        lst: list[Event] = []
        for symbols in cls._interop_symbols.values():
            lst.extend([event for event in symbols if isinstance(event, Event)])

        return lst

    # region Interops

    # Interop Types
    BlockType = BlockType.build()
    Bls12381Type = Bls12381Type.build()
    CallFlagsType = CallFlagsType()
    ContractManifestType = ContractManifestType.build()
    ContractType = ContractType.build()
    FindOptionsType = FindOptionsType()
    Iterator = IteratorType.build()
    NamedCurveHashType = NamedCurveHashType()
    NotificationType = NotificationType.build()
    OracleResponseCode = OracleResponseCodeType.build()
    OracleType = OracleClass.build()
    RoleType = RoleType.build()
    SignerType = SignerType.build()
    StorageContextType = StorageContextType.build()
    StorageMapType = StorageMapType.build()
    TransactionType = TransactionType.build()
    TransactionAttributeType = TransactionAttributeTypeType()
    TriggerType = TriggerTypeType()
    VMStateType = VMStateType.build()
    WitnessCondition = WitnessConditionType.build()
    WitnessConditionType = WitnessConditionEnumType.build()
    WitnessRuleAction = WitnessRuleActionType.build()
    WitnessRule = WitnessRuleType.build()
    WitnessScope = WitnessScopeType.build()

    # Blockchain Interops
    CurrentHash = CurrentHashProperty()
    CurrentIndex = CurrentIndexProperty()
    GetContract = GetContractMethod(ContractType)
    GetBlock = GetBlockMethod(BlockType)
    GetTransaction = GetTransactionMethod(TransactionType)
    GetTransactionFromBlock = GetTransactionFromBlockMethod(TransactionType)
    GetTransactionHeight = GetTransactionHeightMethod()
    GetTransactionSigners = GetTransactionSignersMethod(SignerType)
    GetTransactionVMState = GetTransactionVMStateMethod(VMStateType)

    # Contract Interops
    CallContract = CallMethod()
    CreateContract = CreateMethod(ContractType)
    CreateMultisigAccount = CreateMultisigAccountMethod()
    CreateStandardAccount = CreateStandardAccountMethod()
    DestroyContract = DestroyMethod()
    GetCallFlags = GetCallFlagsMethod(CallFlagsType)
    GetMinimumDeploymentFee = GetMinimumDeploymentFeeMethod()
    UpdateContract = UpdateMethod()

    # Native Contracts
    GasScriptHash = GasToken
    NeoScriptHash = NeoToken
    ContractManagementScriptHash = ContractManagement
    CryptoLibScriptHash = CryptoLibContract
    LedgerScriptHash = LedgerContract
    OracleScriptHash = OracleContract
    StdLibScriptHash = StdLibContract

    # Crypto Interops
    Bls12381Add = Bls12381AddMethod()
    Bls12381Deserialize = Bls12381DeserializeMethod()
    Bls12381Equal = Bls12381EqualMethod()
    Bls12381Mul = Bls12381MulMethod()
    Bls12381Pairing = Bls12381PairingMethod()
    Bls12381Serialize = Bls12381SerializeMethod()
    CheckMultisig = CheckMultisigMethod()
    CheckSig = CheckSigMethod()
    Hash160 = Hash160Method()
    Hash256 = Hash256Method()
    Keccak256 = Keccak256Method()
    Murmur32 = Murmur32Method()
    Ripemd160 = Ripemd160Method()
    Sha256 = Sha256Method()
    VerifyWithECDsa = VerifyWithECDsaMethod()

    # Iterator Interops
    IteratorCreate = IteratorMethod(Iterator)
    IteratorNext = IteratorNextMethod()
    IteratorValue = IteratorValueMethod(Iterator)

    # Json Interops
    JsonDeserialize = JsonDeserializeMethod()
    JsonSerialize = JsonSerializeMethod()

    # Policy Interops
    GetExecFeeFactor = GetExecFeeFactorMethod()
    GetFeePerByte = GetFeePerByteMethod()
    GetStoragePrice = GetStoragePriceMethod()
    GetAttributeFee = GetAttributeFeeMethod(TransactionAttributeType)
    IsBlocked = IsBlockedMethod()
    SetAttributeFee = SetAttributeFeeMethod(TransactionAttributeType)

    # Role Interops
    GetDesignatedByRole = GetDesignatedByRoleMethod()

    # Runtime Interops
    AddressVersion = AddressVersionProperty()
    BlockTime = BlockTimeProperty()
    BurnGas = BurnGasMethod()
    CallingScriptHash = CallingScriptHashProperty()
    CheckWitness = CheckWitnessMethod()
    EntryScriptHash = EntryScriptHashProperty()
    ExecutingScriptHash = ExecutingScriptHashProperty()
    GasLeft = GasLeftProperty()
    GetNetwork = GetNetworkMethod()
    GetNotifications = GetNotificationsMethod(NotificationType)
    GetCurrentSigners = GetCurrentSignersMethod(SignerType)
    GetRandom = GetRandomMethod()
    GetTrigger = GetTriggerMethod(TriggerType)
    InvocationCounter = InvocationCounterProperty()
    LoadScript = LoadScriptMethod()
    Log = LogMethod()
    Notify = NotifyMethod()
    Platform = PlatformProperty()
    ScriptContainer = ScriptContainerProperty()

    # Stdlib Interops
    Atoi = AtoiMethod()
    Base58CheckDecode = Base58CheckDecodeMethod()
    Base58CheckEncode = Base58CheckEncodeMethod()
    Base58Encode = Base58EncodeMethod()
    Base58Decode = Base58DecodeMethod()
    Base64Encode = Base64EncodeMethod()
    Base64Decode = Base64DecodeMethod()
    Deserialize = DeserializeMethod()
    Itoa = ItoaMethod()
    MemoryCompare = MemoryCompareMethod()
    MemorySearch = MemorySearchMethod()
    Serialize = SerializeMethod()

    # Storage Interops
    StorageDelete = StorageDeleteMethod()
    StorageFind = StorageFindMethod(FindOptionsType)
    StorageGetContext = StorageGetContextMethod(StorageContextType)
    StorageGetReadOnlyContext = StorageGetReadOnlyContextMethod(StorageContextType)
    StorageGet = StorageGetBytesMethod()
    StorageGetInt = StorageGetIntMethod()
    StorageGetBool = StorageGetBoolMethod()
    StorageGetStr = StorageGetStrMethod()
    StorageGetList = StorageGetListMethod()
    StorageGetDict = StorageGetDictMethod()
    StorageGetObject = StorageGetObjectMethod()
    StorageGetUInt160 = StorageGetUInt160Method()
    StorageGetUInt256 = StorageGetUInt256Method()
    StorageGetECPoint = StorageGetECPointMethod()
    StorageGetCheck = StorageTryGetBytesMethod()
    StorageGetCheckInt = StorageTryGetIntMethod()
    StorageGetCheckBool = StorageTryGetBoolMethod()
    StorageGetCheckStr = StorageTryGetStrMethod()
    StorageGetCheckList = StorageTryGetListMethod()
    StorageGetCheckDict = StorageTryGetDictMethod()
    StorageGetCheckObject = StorageTryGetObjectMethod()
    StorageGetCheckUInt160 = StorageTryGetUInt160Method()
    StorageGetCheckUInt256 = StorageTryGetUInt256Method()
    StorageGetCheckECPoint = StorageTryGetECPointMethod()
    StoragePut = StoragePutBytesMethod()
    StoragePutInt = StoragePutIntMethod()
    StoragePutBool = StoragePutBoolMethod()
    StoragePutStr = StoragePutStrMethod()
    StoragePutList = StoragePutListMethod()
    StoragePutDict = StoragePutDictMethod()
    StoragePutObject = StoragePutObjectMethod()
    StoragePutUInt160 = StoragePutUInt160Method()
    StoragePutUInt256 = StoragePutUInt256Method()
    StoragePutECPoint = StoragePutECPointMethod()

    # endregion

    # region Packages

    BlockModule = Package(deprecated=True,
                          new_location='boa3.sc.types',
                          identifier=BlockType.identifier.lower(),
                          types=[BlockType]
                          )

    SignerModule = Package(deprecated=True,
                           new_location='boa3.sc.types',
                           identifier=SignerType.identifier.lower(),
                           types=[SignerType,
                                  WitnessConditionType,
                                  WitnessCondition,
                                  WitnessRuleAction,
                                  WitnessRule,
                                  WitnessScope
                                  ]
                           )

    TransactionModule = Package(deprecated=True,
                                new_location='boa3.sc.types',
                                identifier=TransactionType.identifier.lower(),
                                types=[TransactionType]
                                )

    VMStateModule = Package(deprecated=True,
                            new_location='boa3.sc.types',
                            identifier=VMStateType.identifier.lower(),
                            types=[VMStateType]
                            )

    BlockchainPackage = Package(deprecated=True,
                                new_location='boa3.sc.contracts and boa3.sc.types',
                                identifier=InteropPackage.Blockchain,
                                types=[BlockType,
                                       SignerType,
                                       TransactionType,
                                       VMStateType
                                       ],
                                methods=[CurrentHash,
                                         CurrentIndex,
                                         GetBlock,
                                         GetContract,
                                         GetTransaction,
                                         GetTransactionFromBlock,
                                         GetTransactionHeight,
                                         GetTransactionSigners,
                                         GetTransactionVMState
                                         ],
                                packages=[BlockModule,
                                          SignerModule,
                                          TransactionModule,
                                          VMStateModule
                                          ]
                                )

    CallFlagsTypeModule = Package(deprecated=True,
                                  new_location='boa3.sc.types',
                                  identifier=f'{CallFlagsType.identifier.lower()}type',
                                  types=[CallFlagsType]
                                  )

    ContractModule = Package(deprecated=True,
                             new_location='boa3.sc.types',
                             identifier=ContractType.identifier.lower(),
                             types=[ContractType]
                             )

    ContractManifestModule = Package(deprecated=True,
                                     new_location='boa3.sc.types',
                                     identifier=ContractManifestType.identifier.lower(),
                                     types=[ContractAbiType.build(),
                                            ContractEventDescriptorType.build(),
                                            ContractGroupType.build(),
                                            ContractManifestType,
                                            ContractMethodDescriptorType.build(),
                                            ContractParameterDefinitionType.build(),
                                            ContractParameterTypeType.build(),
                                            ContractPermissionDescriptorType.build(),
                                            ContractPermissionType.build()
                                            ]
                                     )

    ContractPackage = Package(deprecated=True,
                              new_location='boa3.sc.contracts, boa3.sc.utils and boa3.sc.types',
                              identifier=InteropPackage.Contract,
                              types=[CallFlagsType,
                                     ContractManifestType,
                                     ContractType
                                     ],
                              properties=[GasScriptHash,
                                          NeoScriptHash
                                          ],
                              methods=[CallContract,
                                       CreateContract,
                                       CreateMultisigAccount,
                                       CreateStandardAccount,
                                       DestroyContract,
                                       GetCallFlags,
                                       GetMinimumDeploymentFee,
                                       UpdateContract
                                       ],
                              packages=[CallFlagsTypeModule,
                                        ContractManifestModule,
                                        ContractModule
                                        ]
                              )

    CryptoPackage = Package(deprecated=True,
                            new_location='boa3.sc.contracts, boa3.sc.utils and boa3.sc.types',
                            identifier=InteropPackage.Crypto,
                            types=[NamedCurveHashType,
                                   Bls12381Type
                                   ],
                            methods=[Bls12381Add,
                                     Bls12381Deserialize,
                                     Bls12381Equal,
                                     Bls12381Mul,
                                     Bls12381Pairing,
                                     Bls12381Serialize,
                                     CheckMultisig,
                                     CheckSig,
                                     Hash160,
                                     Hash256,
                                     Murmur32,
                                     Ripemd160,
                                     Sha256,
                                     VerifyWithECDsa,
                                     ]
                            )

    IteratorPackage = Package(deprecated=True,
                              new_location='boa3.sc.utils',
                              identifier=InteropPackage.Iterator,
                              types=[Iterator],
                              )

    JsonPackage = Package(deprecated=True,
                          new_location='boa3.sc.contracts',
                          identifier=InteropPackage.Json,
                          methods=[JsonDeserialize,
                                   JsonSerialize
                                   ]
                          )

    NotificationModule = Package(deprecated=True,
                                 new_location='boa3.sc.types',
                                 identifier=NotificationType.identifier.lower(),
                                 types=[NotificationType]
                                 )

    OracleResponseCodeModule = Package(deprecated=True,
                                       new_location='boa3.sc.types',
                                       identifier=OracleResponseCode.identifier.lower(),
                                       types=[OracleResponseCode]
                                       )

    OracleModule = Package(deprecated=True,
                           new_location='boa3.sc.contracts',
                           identifier=OracleType.identifier.lower(),
                           types=[OracleType]
                           )

    OraclePackage = Package(deprecated=True,
                            new_location='boa3.sc.contracts and boa3.sc.types',
                            identifier=InteropPackage.Oracle,
                            types=[OracleResponseCode,
                                   OracleType
                                   ],
                            packages=[OracleModule,
                                      OracleResponseCodeModule
                                      ]
                            )

    TriggerTypeModule = Package(deprecated=True,
                                new_location='boa3.sc.types',
                                identifier=TriggerType.identifier.lower(),
                                types=[TriggerType]
                                )

    PolicyPackage = Package(deprecated=True,
                            new_location='boa3.sc.contracts',
                            identifier=InteropPackage.Policy,
                            methods=[GetExecFeeFactor,
                                     GetFeePerByte,
                                     GetStoragePrice,
                                     IsBlocked
                                     ]
                            )

    RoleTypeModule = Package(deprecated=True,
                             new_location='boa3.sc.types',
                             identifier=RoleType.identifier.lower(),
                             types=[RoleType]
                             )

    RolePackage = Package(deprecated=True,
                          new_location='boa3.sc.contracts',
                          identifier=InteropPackage.Role,
                          types=[RoleType],
                          methods=[GetDesignatedByRole],
                          packages=[RoleTypeModule]
                          )

    RuntimePackage = Package(deprecated=True,
                             new_location='boa3.sc.runtime and boa3.sc.types',
                             identifier=InteropPackage.Runtime,
                             types=[NotificationType,
                                    TriggerType
                                    ],
                             properties=[AddressVersion,
                                         BlockTime,
                                         CallingScriptHash,
                                         ExecutingScriptHash,
                                         GasLeft,
                                         Platform,
                                         InvocationCounter,
                                         EntryScriptHash,
                                         ScriptContainer
                                         ],
                             methods=[BurnGas,
                                      CheckWitness,
                                      GetNetwork,
                                      GetNotifications,
                                      GetRandom,
                                      GetTrigger,
                                      LoadScript,
                                      Log,
                                      Notify,
                                      GetCurrentSigners
                                      ],
                             packages=[NotificationModule,
                                       TriggerTypeModule
                                       ]
                             )

    FindOptionsModule = Package(deprecated=True,
                                new_location='boa3.sc.types',
                                identifier=FindOptionsType.identifier.lower(),
                                types=[FindOptionsType]
                                )

    StdlibPackage = Package(deprecated=True,
                            new_location='boa3.sc.contracts',
                            identifier=InteropPackage.Stdlib,
                            methods=[Atoi,
                                     Base58CheckDecode,
                                     Base58CheckEncode,
                                     Base58Encode,
                                     Base58Decode,
                                     Base64Encode,
                                     Base64Decode,
                                     Deserialize,
                                     Itoa,
                                     MemoryCompare,
                                     MemorySearch,
                                     Serialize
                                     ]
                            )

    StorageContextModule = Package(deprecated=True,
                                   new_location='boa3.sc.storage',
                                   identifier=StorageContextType.identifier.lower(),
                                   types=[StorageContextType]
                                   )

    StorageMapModule = Package(deprecated=True,
                               new_location='boa3.sc.storage',
                               identifier=StorageMapType.identifier.lower(),
                               types=[StorageMapType]
                               )

    StoragePackage = Package(deprecated=True,
                             new_location='boa3.sc.storage',
                             identifier=InteropPackage.Storage,
                             types=[FindOptionsType,
                                    StorageContextType,
                                    StorageMapType
                                    ],
                             methods=[StorageDelete,
                                      StorageFind,
                                      StorageGet,
                                      StorageGetInt,
                                      StorageGetBool,
                                      StorageGetStr,
                                      StorageGetList,
                                      StorageGetDict,
                                      StorageGetObject,
                                      StorageGetUInt160,
                                      StorageGetUInt256,
                                      StorageGetECPoint,
                                      StorageGetCheck,
                                      StorageGetCheckInt,
                                      StorageGetCheckBool,
                                      StorageGetCheckStr,
                                      StorageGetCheckList,
                                      StorageGetCheckDict,
                                      StorageGetCheckObject,
                                      StorageGetCheckUInt160,
                                      StorageGetCheckUInt256,
                                      StorageGetCheckECPoint,
                                      StorageGetContext,
                                      StorageGetReadOnlyContext,
                                      StoragePut,
                                      StoragePutInt,
                                      StoragePutBool,
                                      StoragePutStr,
                                      StoragePutList,
                                      StoragePutDict,
                                      StoragePutObject,
                                      StoragePutUInt160,
                                      StoragePutUInt256,
                                      StoragePutECPoint,
                                      ],
                             packages=[FindOptionsModule,
                                       StorageContextModule,
                                       StorageMapModule
                                       ]
                             )

    # endregion

    package_symbols: list[IdentifiedSymbol] = [
        OracleType,
        BlockchainPackage,
        ContractPackage,
        CryptoPackage,
        IteratorPackage,
        JsonPackage,
        OraclePackage,
        PolicyPackage,
        RolePackage,
        RuntimePackage,
        StdlibPackage,
        StoragePackage
    ]

    _interop_symbols: dict[InteropPackage, list[IdentifiedSymbol]] = {
        package.identifier: list(package.symbols.values()) for package in package_symbols if
        isinstance(package, Package)
    }
