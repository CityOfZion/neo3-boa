from enum import Enum
from typing import Dict, List

from boa3.model.builtin.interop.binary.base58decodemethod import Base58DecodeMethod
from boa3.model.builtin.interop.binary.base58encodemethod import Base58EncodeMethod
from boa3.model.builtin.interop.binary.base64decodemethod import Base64DecodeMethod
from boa3.model.builtin.interop.binary.base64encodemethod import Base64EncodeMethod
from boa3.model.builtin.interop.blockchain.getcurrentheightmethod import CurrentHeightProperty
from boa3.model.builtin.interop.contract.createmethod import CreateMethod
from boa3.model.builtin.interop.contract.callmethod import CallMethod
from boa3.model.builtin.interop.contract.getgasscripthashmethod import GasProperty
from boa3.model.builtin.interop.contract.getneoscripthashmethod import NeoProperty
from boa3.model.builtin.interop.runtime.checkwitnessmethod import CheckWitnessMethod
from boa3.model.builtin.interop.runtime.getblocktimemethod import BlockTimeProperty
from boa3.model.builtin.interop.runtime.getcallingscripthashmethod import CallingScriptHashProperty
from boa3.model.builtin.interop.runtime.getexecutingscripthashmethod import ExecutingScriptHashProperty
from boa3.model.builtin.interop.runtime.getgasleftmethod import GasLeftProperty
from boa3.model.builtin.interop.runtime.getinvocationcountermethod import InvocationCounterProperty
from boa3.model.builtin.interop.runtime.logmethod import LogMethod
from boa3.model.builtin.interop.runtime.notifymethod import NotifyMethod
from boa3.model.builtin.interop.runtime.triggermethod import TriggerMethod
from boa3.model.builtin.interop.runtime.triggertype import TriggerType as TriggerTyping
from boa3.model.builtin.interop.storage.storagedeletemethod import StorageDeleteMethod
from boa3.model.builtin.interop.storage.storagegetmethod import StorageGetMethod
from boa3.model.builtin.interop.storage.storageputmethod import StoragePutMethod
from boa3.model.builtin.interop.crypto.sha256method import Sha256Method
from boa3.model.builtin.interop.crypto.ripemd160method import Ripemd160Method
from boa3.model.builtin.interop.crypto.hash160method import Hash160Method
from boa3.model.builtin.interop.crypto.hash256method import Hash256Method
from boa3.model.builtin.interop.crypto.checkmultisigwithecdsasecp256r1method import CheckMultisigWithECDsaSecp256r1Method
from boa3.model.builtin.interop.crypto.checkmultisigwithecdsasecp256k1method import CheckMultisigWithECDsaSecp256k1Method
from boa3.model.builtin.interop.crypto.verifywithecdsasecp256r1 import VerifyWithECDsaSecp256r1Method
from boa3.model.builtin.interop.crypto.verifywithecdsasecp256k1 import VerifyWithECDsaSecp256k1Method
from boa3.model.identifiedsymbol import IdentifiedSymbol


class InteropPackage(str, Enum):
    Binary = 'binary'
    Blockchain = 'blockchain'
    Contract = 'contract'
    Crypto = 'crypto'
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
    Base58Encode = Base58EncodeMethod()
    Base58Decode = Base58DecodeMethod()
    Base64Encode = Base64EncodeMethod()
    Base64Decode = Base64DecodeMethod()

    # Blockchain Interops
    CurrentHeight = CurrentHeightProperty()

    # Contract Interops
    CreateContract = CreateMethod()
    CallContract = CallMethod()
    NeoScriptHash = NeoProperty()
    GasScriptHash = GasProperty()

    # Runtime Interops
    CheckWitness = CheckWitnessMethod()
    Notify = NotifyMethod()
    Log = LogMethod()
    TriggerType = TriggerTyping()
    GetTrigger = TriggerMethod(TriggerType)
    CallingScriptHash = CallingScriptHashProperty()
    ExecutingScriptHash = ExecutingScriptHashProperty()
    BlockTime = BlockTimeProperty()
    GasLeft = GasLeftProperty()
    InvocationCounter = InvocationCounterProperty()

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
                                Base64Decode
                                ],
        InteropPackage.Blockchain: [CurrentHeight
                                    ],
        InteropPackage.Contract: [CallContract,
                                  CreateContract,
                                  NeoScriptHash,
                                  GasScriptHash
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
        InteropPackage.Runtime: [CheckWitness,
                                 Notify,
                                 Log,
                                 TriggerType,
                                 GetTrigger,
                                 CallingScriptHash,
                                 ExecutingScriptHash,
                                 BlockTime,
                                 GasLeft,
                                 InvocationCounter
                                 ],
        InteropPackage.Storage: [StorageGet,
                                 StoragePut,
                                 StorageDelete
                                 ]
    }
