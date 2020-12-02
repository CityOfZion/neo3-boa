from enum import Enum
from typing import Dict, List

from boa3.model.builtin.interop.binary import *
from boa3.model.builtin.interop.blockchain import *
from boa3.model.builtin.interop.contract import *
from boa3.model.builtin.interop.crypto import *
from boa3.model.builtin.interop.iterator import *
from boa3.model.builtin.interop.json import *
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

    # Binary Interops
    Serialize = SerializeMethod()
    Deserialize = DeserializeMethod()
    Base58Encode = Base58EncodeMethod()
    Base58Decode = Base58DecodeMethod()
    Base64Encode = Base64EncodeMethod()
    Base64Decode = Base64DecodeMethod()

    # Blockchain Interops
    CurrentHeight = CurrentHeightProperty()

    # Contract Interops
    ContractType = ContractType.build()
    CreateContract = CreateMethod(ContractType)
    CallContract = CallMethod()
    UpdateContract = UpdateMethod()
    DestroyContract = DestroyMethod()
    NeoScriptHash = NeoProperty()
    GasScriptHash = GasProperty()

    # Iterator Interops
    Iterator = IteratorType.build()
    IteratorCreate = IteratorMethod(Iterator)

    # Json Interops
    JsonDeserialize = JsonDeserializeMethod()
    JsonSerialize = JsonSerializeMethod()

    # Runtime Interops
    CheckWitness = CheckWitnessMethod()
    Notify = NotifyMethod()
    Log = LogMethod()
    TriggerType = TriggerType()
    GetTrigger = TriggerMethod(TriggerType)
    CallingScriptHash = CallingScriptHashProperty()
    ExecutingScriptHash = ExecutingScriptHashProperty()
    Platform = PlatformProperty()
    BlockTime = BlockTimeProperty()
    GasLeft = GasLeftProperty()
    InvocationCounter = InvocationCounterProperty()
    NotificationType = NotificationType.build()
    GetNotifications = GetNotificationsMethod(NotificationType)
    EntryScriptHash = EntryScriptHashProperty()

    # Storage Interops
    StorageGet = StorageGetMethod()
    StoragePut = StoragePutMethod()
    StorageDelete = StorageDeleteMethod()

    # Crypto Interops
    Sha256 = Sha256Method()
    Ripemd160 = Ripemd160Method()
    Hash160 = Hash160Method()
    Hash256 = Hash256Method()
    CheckMultisigWithECDsaSecp256r1 = CheckMultisigWithECDsaSecp256r1Method()
    CheckMultisigWithECDsaSecp256k1 = CheckMultisigWithECDsaSecp256k1Method()
    VerifyWithECDsaSecp256r1 = VerifyWithECDsaSecp256r1Method()
    VerifyWithECDsaSecp256k1 = VerifyWithECDsaSecp256k1Method()

    _interop_symbols: Dict[InteropPackage, List[IdentifiedSymbol]] = {
        InteropPackage.Binary: [Base58Encode,
                                Base58Decode,
                                Base64Encode,
                                Base64Decode,
                                Deserialize,
                                Serialize
                                ],
        InteropPackage.Blockchain: [CurrentHeight
                                    ],
        InteropPackage.Contract: [CreateContract,
                                  CallContract,
                                  UpdateContract,
                                  DestroyContract,
                                  NeoScriptHash,
                                  GasScriptHash,
                                  ContractType
                                  ],
        InteropPackage.Crypto: [Sha256,
                                Ripemd160,
                                Hash160,
                                Hash256,
                                CheckMultisigWithECDsaSecp256r1,
                                CheckMultisigWithECDsaSecp256k1,
                                VerifyWithECDsaSecp256r1,
                                VerifyWithECDsaSecp256k1
                                ],
        InteropPackage.Iterator: [Iterator],
        InteropPackage.Json: [JsonDeserialize,
                              JsonSerialize
                              ],
        InteropPackage.Runtime: [BlockTime,
                                 CallingScriptHash,
                                 CheckWitness,
                                 ExecutingScriptHash,
                                 Platform,
                                 GasLeft,
                                 GetNotifications,
                                 GetTrigger,
                                 InvocationCounter,
                                 Log,
                                 NotificationType,
                                 Notify,
                                 TriggerType,
                                 EntryScriptHash
                                 ],
        InteropPackage.Storage: [StorageGet,
                                 StoragePut,
                                 StorageDelete
                                 ]
    }
