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

    # Interop Types
    BlockType = BlockType.build()
    CallFlagsType = CallFlagsType()
    ContractType = ContractType.build()
    Iterator = IteratorType.build()
    NotificationType = NotificationType.build()
    OracleType = OracleType.build()
    StorageContextType = StorageContextType.build()
    StorageMapType = StorageMapType.build()
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

    # Storage Interops
    StorageDelete = StorageDeleteMethod()
    StorageFind = StorageFindMethod()
    StorageGetContext = StorageGetContextMethod(StorageContextType)
    StorageGet = StorageGetMethod()
    StoragePut = StoragePutMethod()

    _interop_symbols: Dict[InteropPackage, List[IdentifiedSymbol]] = {
        InteropPackage.Binary: [Atoi,
                                Base58Encode,
                                Base58Decode,
                                Base64Encode,
                                Base64Decode,
                                Deserialize,
                                Itoa,
                                Serialize
                                ],
        InteropPackage.Blockchain: [BlockType,
                                    CurrentHeight,
                                    GetBlock,
                                    GetContract
                                    ],
        InteropPackage.Contract: [CallContract,
                                  CallFlagsType,
                                  ContractType,
                                  CreateContract,
                                  DestroyContract,
                                  GasScriptHash,
                                  GetCallFlags,
                                  NeoScriptHash,
                                  UpdateContract
                                  ],
        InteropPackage.Crypto: [CheckMultisig,
                                Hash160,
                                Hash256,
                                Ripemd160,
                                Sha256,
                                VerifyWithECDsaSecp256k1,
                                VerifyWithECDsaSecp256r1
                                ],
        InteropPackage.Iterator: [Iterator],
        InteropPackage.Json: [JsonDeserialize,
                              JsonSerialize
                              ],
        InteropPackage.Runtime: [BlockTime,
                                 CallingScriptHash,
                                 CheckWitness,
                                 EntryScriptHash,
                                 ExecutingScriptHash,
                                 GasLeft,
                                 GetNotifications,
                                 GetTrigger,
                                 InvocationCounter,
                                 Log,
                                 NotificationType,
                                 Notify,
                                 Platform,
                                 TriggerType
                                 ],
        InteropPackage.Storage: [StorageContextType,
                                 StorageDelete,
                                 StorageFind,
                                 StorageGet,
                                 StorageGetContext,
                                 StorageMapType,
                                 StoragePut
                                 ]
    }
    package_symbols: List[IdentifiedSymbol] = [
        OracleType
    ]
