from enum import Enum
from typing import Dict, List

from boa3.model.builtin.interop import *
from boa3.model.builtin.interop.binary import *
from boa3.model.builtin.interop.blockchain import *
from boa3.model.builtin.interop.contract import *
from boa3.model.builtin.interop.crypto import *
from boa3.model.builtin.interop.iterator import *
from boa3.model.builtin.interop.json import *
from boa3.model.builtin.interop.nativecontract import *
from boa3.model.builtin.interop.runtime import *
from boa3.model.builtin.interop.storage import *
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.imports.package import Package


class InteropPackage(str, Enum):
    Binary = 'binary'
    Blockchain = 'blockchain'
    Contract = 'contract'
    Crypto = 'crypto'
    Iterator = 'iterator'
    Json = 'json'
    Runtime = 'runtime'
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
    ContractType = ContractType.build()
    Iterator = IteratorType.build()
    NotificationType = NotificationType.build()
    OracleType = OracleType.build()
    StorageContextType = StorageContextType.build()
    StorageMapType = StorageMapType.build()
    TransactionType = TransactionType.build()
    TriggerType = TriggerType()

    # Binary Interops
    Atoi = AtoiMethod()
    Base58Encode = Base58EncodeMethod()
    Base58Decode = Base58DecodeMethod()
    Base64Encode = Base64EncodeMethod()
    Base64Decode = Base64DecodeMethod()
    Deserialize = DeserializeMethod()
    Itoa = ItoaMethod()
    Serialize = SerializeMethod()

    # Blockchain Interops
    CurrentHeight = CurrentHeightProperty()
    GetContract = GetContractMethod(ContractType)
    GetBlock = GetBlockMethod(BlockType)
    GetTransaction = GetTransactionMethod(TransactionType)
    GetTransactionFromBlock = GetTransactionFromBlockMethod(TransactionType)
    GetTransactionHeight = GetTransactionHeightMethod()

    # Contract Interops
    CallContract = CallMethod()
    CreateContract = CreateMethod(ContractType)
    DestroyContract = DestroyMethod()
    GetCallFlags = GetCallFlagsMethod(CallFlagsType)
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
    Hash160 = Hash160Method()
    Hash256 = Hash256Method()
    Ripemd160 = Ripemd160Method()
    Sha256 = Sha256Method()
    VerifyWithECDsaSecp256k1 = VerifyWithECDsaSecp256k1Method()
    VerifyWithECDsaSecp256r1 = VerifyWithECDsaSecp256r1Method()

    # Iterator Interops
    IteratorCreate = IteratorMethod(Iterator)

    # Json Interops
    JsonDeserialize = JsonDeserializeMethod()
    JsonSerialize = JsonSerializeMethod()

    # Runtime Interops
    BlockTime = BlockTimeProperty()
    BurnGas = BurnGasMethod()
    CallingScriptHash = CallingScriptHashProperty()
    CheckWitness = CheckWitnessMethod()
    EntryScriptHash = EntryScriptHashProperty()
    ExecutingScriptHash = ExecutingScriptHashProperty()
    GasLeft = GasLeftProperty()
    GetNotifications = GetNotificationsMethod(NotificationType)
    GetTrigger = GetTriggerMethod(TriggerType)
    InvocationCounter = InvocationCounterProperty()
    Log = LogMethod()
    Notify = NotifyMethod()
    Platform = PlatformProperty()
    ScriptContainer = ScriptContainerProperty()

    # Storage Interops
    StorageDelete = StorageDeleteMethod()
    StorageFind = StorageFindMethod()
    StorageGetContext = StorageGetContextMethod(StorageContextType)
    StorageGet = StorageGetMethod()
    StoragePut = StoragePutMethod()

    # endregion

    # region Packages

    BinaryPackage = Package(identifier=InteropPackage.Binary,
                            methods=[Atoi,
                                     Base58Encode,
                                     Base58Decode,
                                     Base64Encode,
                                     Base64Decode,
                                     Deserialize,
                                     Itoa,
                                     Serialize
                                     ]
                            )

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
                                methods=[CurrentHeight,
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

    ContractPackage = Package(identifier=InteropPackage.Contract,
                              types=[CallFlagsType,
                                     ContractType
                                     ],
                              properties=[GasScriptHash,
                                          NeoScriptHash
                                          ],
                              methods=[CallContract,
                                       CreateContract,
                                       DestroyContract,
                                       GetCallFlags,
                                       UpdateContract
                                       ],
                              packages=[CallFlagsTypeModule,
                                        ContractModule
                                        ]
                              )

    CryptoPackage = Package(identifier=InteropPackage.Crypto,
                            methods=[CheckMultisig,
                                     Hash160,
                                     Hash256,
                                     Ripemd160,
                                     Sha256,
                                     VerifyWithECDsaSecp256k1,
                                     VerifyWithECDsaSecp256r1
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

    TriggerTypeModule = Package(identifier=TriggerType.identifier.lower(),
                                types=[TriggerType]
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
                                      GetNotifications,
                                      GetTrigger,
                                      Log,
                                      Notify
                                      ],
                             packages=[NotificationModule,
                                       TriggerTypeModule
                                       ]
                             )

    StorageContextModule = Package(identifier=StorageContextType.identifier.lower(),
                                   types=[StorageContextType]
                                   )
    StorageMapModule = Package(identifier=StorageMapType.identifier.lower(),
                               types=[StorageMapType]
                               )

    StoragePackage = Package(identifier=InteropPackage.Storage,
                             types=[StorageContextType,
                                    StorageMapType
                                    ],
                             methods=[StorageDelete,
                                      StorageFind,
                                      StorageGet,
                                      StorageGetContext,
                                      StoragePut
                                      ],
                             packages=[StorageContextModule,
                                       StorageMapModule
                                       ]
                             )

    # endregion

    package_symbols: List[IdentifiedSymbol] = [
        OracleType,
        BinaryPackage,
        BlockchainPackage,
        ContractPackage,
        CryptoPackage,
        IteratorPackage,
        JsonPackage,
        RuntimePackage,
        StoragePackage
    ]

    _interop_symbols: Dict[InteropPackage, List[IdentifiedSymbol]] = {
        package.identifier: list(package.symbols.values()) for package in package_symbols if
        isinstance(package, Package)
    }
