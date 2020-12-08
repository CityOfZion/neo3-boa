from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from boa3.model.builtin.builtincallable import IBuiltinCallable
from boa3.model.builtin.classmethod.appendmethod import AppendMethod
from boa3.model.builtin.classmethod.clearmethod import ClearMethod
from boa3.model.builtin.classmethod.extendmethod import ExtendMethod
from boa3.model.builtin.classmethod.mapkeysmethod import MapKeysMethod
from boa3.model.builtin.classmethod.mapvaluesmethod import MapValuesMethod
from boa3.model.builtin.classmethod.popmethod import PopMethod
from boa3.model.builtin.classmethod.reversemethod import ReverseMethod
from boa3.model.builtin.classmethod.tobytesmethod import ToBytes as ToBytesMethod
from boa3.model.builtin.classmethod.tointmethod import ToInt as ToIntMethod
from boa3.model.builtin.classmethod.tostrmethod import ToStr as ToStrMethod
from boa3.model.builtin.contract.abortmethod import AbortMethod
from boa3.model.builtin.contract.nep5transferevent import Nep5TransferEvent
from boa3.model.builtin.decorator.metadatadecorator import MetadataDecorator
from boa3.model.builtin.decorator.publicdecorator import PublicDecorator
from boa3.model.builtin.interop.interop import Interop
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.builtin.method.bytearraymethod import ByteArrayMethod
from boa3.model.builtin.method.createeventmethod import CreateEventMethod, EventType
from boa3.model.builtin.method.exceptionmethod import ExceptionMethod
from boa3.model.builtin.method.isinstancemethod import IsInstanceMethod
from boa3.model.builtin.method.lenmethod import LenMethod
from boa3.model.builtin.method.printmethod import PrintMethod
from boa3.model.builtin.method.rangemethod import RangeMethod
from boa3.model.builtin.method.toscripthashmethod import ScriptHashMethod
from boa3.model.builtin.neometadatatype import MetadataTypeSingleton as NeoMetadataType
from boa3.model.callable import Callable
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.symbol import ISymbol
from boa3.model.type.collection.sequence.uint160type import UInt160Type
from boa3.model.type.itype import IType


class BoaPackage(str, Enum):
    Contract = 'contract'
    Type = 'type'


class Builtin:
    @classmethod
    def get_symbol(cls, symbol_id: str) -> Optional[Callable]:
        for name, method in vars(cls).items():
            if isinstance(method, IBuiltinCallable) and method.identifier == symbol_id:
                return method

    @classmethod
    def get_any_symbol(cls, symbol_id: str) -> Optional[ISymbol]:
        for name, method in vars(cls).items():
            if isinstance(method, IdentifiedSymbol) and method.identifier == symbol_id:
                return method

    @classmethod
    def get_by_self(cls, symbol_id: str, self_type: IType) -> Optional[Callable]:
        for name, method in vars(cls).items():
            if (isinstance(method, IBuiltinMethod)
                    and method.identifier == symbol_id
                    and method.validate_self(self_type)):
                return method

    # builtin method
    Len = LenMethod()
    IsInstance = IsInstanceMethod()
    Print = PrintMethod()
    ScriptHash = ScriptHashMethod()
    NewEvent = CreateEventMethod()

    # python builtin class constructor
    ByteArray = ByteArrayMethod()
    Range = RangeMethod()
    Exception = ExceptionMethod()

    # python class method
    SequenceAppend = AppendMethod()
    SequenceClear = ClearMethod()
    SequenceExtend = ExtendMethod()
    SequencePop = PopMethod()
    SequenceReverse = ReverseMethod()
    DictKeys = MapKeysMethod()
    DictValues = MapValuesMethod()

    # custom class methods
    ConvertToBytes = ToBytesMethod
    ConvertToInt = ToIntMethod
    ConvertToStr = ToStrMethod

    _python_builtins: List[IdentifiedSymbol] = [Len,
                                                IsInstance,
                                                Print,
                                                ScriptHash,
                                                ByteArray,
                                                SequenceAppend,
                                                SequenceClear,
                                                SequenceExtend,
                                                SequencePop,
                                                SequenceReverse,
                                                DictKeys,
                                                DictValues,
                                                ConvertToBytes,
                                                ConvertToInt,
                                                ConvertToStr
                                                ]

    @classmethod
    def interop_symbols(cls, package: str = None) -> Dict[str, IdentifiedSymbol]:
        return {symbol.raw_identifier if hasattr(symbol, 'raw_identifier') else symbol.identifier: symbol
                for symbol in Interop.interop_symbols(package)}

    # builtin decorator
    Public = PublicDecorator()
    Metadata = MetadataDecorator()

    # boa builtin type
    Event = EventType
    UInt160 = UInt160Type.build()

    # boa events
    Nep5Transfer = Nep5TransferEvent()

    # boa smart contract methods
    Abort = AbortMethod()

    _boa_builtins: List[IdentifiedSymbol] = [Public,
                                             NewEvent,
                                             Event,
                                             Metadata,
                                             NeoMetadataType,
                                             ScriptHash
                                             ]

    metadata_fields: Dict[str, Union[type, Tuple[type]]] = \
        {
            'author': (str, type(None)),
            'email': (str, type(None)),
            'description': (str, type(None)),
            'has_storage': bool,
            'is_payable': bool
    }

    @classmethod
    def boa_symbols(cls) -> Dict[str, IdentifiedSymbol]:
        return {symbol.identifier: symbol for symbol in cls._boa_builtins}

    @classmethod
    def package_symbols(cls, package: str = None) -> Dict[str, IdentifiedSymbol]:
        if package in BoaPackage.__members__.values():
            return {symbol.identifier: symbol for symbol in cls._boa_symbols[package]}

        return cls.boa_symbols()

    _boa_symbols: Dict[BoaPackage, List[IdentifiedSymbol]] = {
        BoaPackage.Contract: [Nep5Transfer,
                              Abort
                              ],
        BoaPackage.Type: [UInt160]
    }
