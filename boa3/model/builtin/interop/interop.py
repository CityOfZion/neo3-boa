from enum import Enum
from typing import Dict, List

from boa3.model.builtin.interop.blockchain import *
from boa3.model.builtin.interop.contract import *
from boa3.model.builtin.interop.contract.contractmanifest import *
from boa3.model.builtin.interop.crypto import *
from boa3.model.builtin.interop.iterator import *
from boa3.model.builtin.interop.json import *
from boa3.model.builtin.interop.nativecontract import *
from boa3.model.builtin.interop.oracle import *
from boa3.model.builtin.interop.policy import *
from boa3.model.builtin.interop.role import *
from boa3.model.builtin.interop.runtime import *
from boa3.model.builtin.interop.stdlib import *
from boa3.model.builtin.interop.storage import *
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.imports.package import Package


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
    def interop_symbols(cls, package: str = None) -> List[IdentifiedSymbol]:
        if package in InteropPackage.__members__.values():
            return cls._interop_symbols[package]

        lst: List[IdentifiedSymbol] = []
        for symbols in cls._interop_symbols.values():
            lst.extend(symbols)
        return lst

    # region Interops

    # Interop Types
    BlockType = BlockType.build()
    CallFlagsType = CallFlagsType()
    ContractManifestType = ContractManifestType.build()
    ContractType = ContractType.build()
    FindOptionsType = FindOptionsType()
    Iterator = IteratorType.build()
    NamedCurveType = NamedCurveType()
    NotificationType = NotificationType.build()
    OracleResponseCode = OracleResponseCodeType.build()
    OracleType = OracleType.build()
    RoleType = RoleType.build()
    StorageContextType = StorageContextType.build()
    StorageMapType = StorageMapType.build()
    TransactionType = TransactionType.build()
    TriggerType = TriggerType()

    # Blockchain Interops
    CurrentHash = CurrentHashProperty()
    CurrentIndex = CurrentIndexProperty()
    GetContract = GetContractMethod(ContractType)
    GetBlock = GetBlockMethod(BlockType)
    GetTransaction = GetTransactionMethod(TransactionType)
    GetTransactionFromBlock = GetTransactionFromBlockMethod(TransactionType)
    GetTransactionHeight = GetTransactionHeightMethod()

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
    GasScriptHash = GasProperty()
    NeoScriptHash = NeoProperty()
    ContractManagementScriptHash = ContractManagement
    CryptoLibScriptHash = CryptoLibContract
    LedgerScriptHash = LedgerContract
    OracleScriptHash = OracleContract
    StdLibScriptHash = StdLibContract

    # Crypto Interops
    CheckMultisig = CheckMultisigMethod()
    CheckSig = CheckSigMethod()
    Hash160 = Hash160Method()
    Hash256 = Hash256Method()
    Ripemd160 = Ripemd160Method()
    Sha256 = Sha256Method()
    VerifyWithECDsa = VerifyWithECDsaMethod()

    # Iterator Interops
    IteratorCreate = IteratorMethod(Iterator)

    # Json Interops
    JsonDeserialize = JsonDeserializeMethod()
    JsonSerialize = JsonSerializeMethod()

    # Policy Interops
    GetExecFeeFactor = GetExecFeeFactorMethod()
    GetFeePerByte = GetFeePerByteMethod()
    GetStoragePrice = GetStoragePriceMethod()
    IsBlocked = IsBlockedMethod()

    # Role Interops
    GetDesignatedByRole = GetDesignatedByRoleMethod()

    # Runtime Interops
    BlockTime = BlockTimeProperty()
    BurnGas = BurnGasMethod()
    CallingScriptHash = CallingScriptHashProperty()
    CheckWitness = CheckWitnessMethod()
    EntryScriptHash = EntryScriptHashProperty()
    ExecutingScriptHash = ExecutingScriptHashProperty()
    GasLeft = GasLeftProperty()
    GetNetwork = GetNetworkMethod()
    GetNotifications = GetNotificationsMethod(NotificationType)
    GetRandom = GetRandomMethod()
    GetTrigger = GetTriggerMethod(TriggerType)
    InvocationCounter = InvocationCounterProperty()
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
    StorageGet = StorageGetMethod()
    StoragePut = StoragePutMethod()

    # endregion

    # region Packages

    BlockModule = Package(identifier=BlockType.identifier.lower(),
                          types=[BlockType]
                          )

    TransactionModule = Package(identifier=TransactionType.identifier.lower(),
                                types=[TransactionType]
                                )

    BlockchainPackage = Package(identifier=InteropPackage.Blockchain,
                                types=[BlockType,
                                       TransactionType
                                       ],
                                methods=[CurrentHash,
                                         CurrentIndex,
                                         GetBlock,
                                         GetContract,
                                         GetTransaction,
                                         GetTransactionFromBlock,
                                         GetTransactionHeight
                                         ],
                                packages=[BlockModule,
                                          TransactionModule
                                          ]
                                )

    CallFlagsTypeModule = Package(identifier=f'{CallFlagsType.identifier.lower()}type',
                                  types=[CallFlagsType]
                                  )

    ContractModule = Package(identifier=ContractType.identifier.lower(),
                             types=[ContractType]
                             )

    ContractManifestModule = Package(identifier=ContractManifestType.identifier.lower(),
                                     types=[ContractAbiType.build(),
                                            ContractEventDescriptorType.build(),
                                            ContractGroupType.build(),
                                            ContractManifestType,
                                            ContractMethodDescriptorType.build(),
                                            ContractParameterDefinitionType.build(),
                                            ContractParameterType.build(),
                                            ContractPermissionDescriptorType.build(),
                                            ContractPermissionType.build()
                                            ]
                                     )

    ContractPackage = Package(identifier=InteropPackage.Contract,
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

    CryptoPackage = Package(identifier=InteropPackage.Crypto,
                            types=[NamedCurveType],
                            methods=[CheckMultisig,
                                     CheckSig,
                                     Hash160,
                                     Hash256,
                                     Ripemd160,
                                     Sha256,
                                     VerifyWithECDsa,
                                     ]
                            )

    IteratorPackage = Package(identifier=InteropPackage.Iterator,
                              types=[Iterator],
                              )

    JsonPackage = Package(identifier=InteropPackage.Json,
                          methods=[JsonDeserialize,
                                   JsonSerialize
                                   ]
                          )

    NotificationModule = Package(identifier=NotificationType.identifier.lower(),
                                 types=[NotificationType]
                                 )

    OracleResponseCodeModule = Package(identifier=OracleResponseCode.identifier.lower(),
                                       types=[OracleResponseCode]
                                       )

    OracleModule = Package(identifier=OracleType.identifier.lower(),
                           types=[OracleType]
                           )

    OraclePackage = Package(identifier=InteropPackage.Oracle,
                            types=[OracleResponseCode,
                                   OracleType
                                   ],
                            packages=[OracleModule,
                                      OracleResponseCodeModule
                                      ]
                            )

    TriggerTypeModule = Package(identifier=TriggerType.identifier.lower(),
                                types=[TriggerType]
                                )

    PolicyPackage = Package(identifier=InteropPackage.Policy,
                            methods=[GetExecFeeFactor,
                                     GetFeePerByte,
                                     GetStoragePrice,
                                     IsBlocked
                                     ]
                            )

    RolePackage = Package(identifier=InteropPackage.Role,
                          types=[RoleType],
                          methods=[GetDesignatedByRole]
                          )

    RuntimePackage = Package(identifier=InteropPackage.Runtime,
                             types=[NotificationType,
                                    TriggerType
                                    ],
                             properties=[BlockTime,
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
                                      Log,
                                      Notify
                                      ],
                             packages=[NotificationModule,
                                       TriggerTypeModule
                                       ]
                             )

    FindOptionsModule = Package(identifier=FindOptionsType.identifier.lower(),
                                types=[FindOptionsType]
                                )

    StdlibPackage = Package(identifier=InteropPackage.Stdlib,
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

    StorageContextModule = Package(identifier=StorageContextType.identifier.lower(),
                                   types=[StorageContextType]
                                   )

    StorageMapModule = Package(identifier=StorageMapType.identifier.lower(),
                               types=[StorageMapType]
                               )

    StoragePackage = Package(identifier=InteropPackage.Storage,
                             types=[FindOptionsType,
                                    StorageContextType,
                                    StorageMapType
                                    ],
                             methods=[StorageDelete,
                                      StorageFind,
                                      StorageGet,
                                      StorageGetContext,
                                      StorageGetReadOnlyContext,
                                      StoragePut
                                      ],
                             packages=[FindOptionsModule,
                                       StorageContextModule,
                                       StorageMapModule
                                       ]
                             )

    # endregion

    package_symbols: List[IdentifiedSymbol] = [
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

    _interop_symbols: Dict[InteropPackage, List[IdentifiedSymbol]] = {
        package.identifier: list(package.symbols.values()) for package in package_symbols if
        isinstance(package, Package)
    }
