from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from boa3.model.builtin.builtincallable import IBuiltinCallable
from boa3.model.builtin.classmethod import *
from boa3.model.builtin.contract import *
from boa3.model.builtin.decorator.metadatadecorator import MetadataDecorator
from boa3.model.builtin.decorator.publicdecorator import PublicDecorator
from boa3.model.builtin.interop.interop import Interop
from boa3.model.builtin.method import *
from boa3.model.builtin.neometadatatype import MetadataTypeSingleton as NeoMetadataType
from boa3.model.callable import Callable
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.symbol import ISymbol
from boa3.model.type.collection.sequence.uint160type import UInt160Type
from boa3.model.type.collection.sequence.uint256type import UInt256Type
from boa3.model.type.itype import IType


class BoaPackage(str, Enum):
    Contract = 'contract'
    Interop = 'interop'
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
    Abs = AbsMethod()
    Exit = ExitMethod()
    IsInstance = IsInstanceMethod()
    Len = LenMethod()
    NewEvent = CreateEventMethod()
    Max = MaxMethod()
    Min = MinMethod()
    Print = PrintMethod()
    ScriptHash = ScriptHashMethod()
    Sqrt = SqrtMethod()
    Sum = SumMethod()

    # python builtin class constructor
    ByteArray = ByteArrayMethod()
    Range = RangeMethod()
    Exception = ExceptionMethod()

    # python class method
    SequenceAppend = AppendMethod()
    SequenceClear = ClearMethod()
    SequenceExtend = ExtendMethod()
    SequenceInsert = InsertMethod()
    SequencePop = PopMethod()
    SequenceRemove = RemoveMethod()
    SequenceReverse = ReverseMethod()
    DictKeys = MapKeysMethod()
    DictValues = MapValuesMethod()

    # custom class methods
    ConvertToBytes = ToBytesMethod
    ConvertToInt = ToIntMethod
    ConvertToStr = ToStrMethod
    ConvertToBool = ToBoolMethod

    _python_builtins: List[IdentifiedSymbol] = [Abs,
                                                ByteArray,
                                                ConvertToBool,
                                                ConvertToBytes,
                                                ConvertToInt,
                                                ConvertToStr,
                                                DictKeys,
                                                DictValues,
                                                Exit,
                                                IsInstance,
                                                Len,
                                                Max,
                                                Min,
                                                Print,
                                                ScriptHash,
                                                SequenceAppend,
                                                SequenceClear,
                                                SequenceExtend,
                                                SequenceInsert,
                                                SequencePop,
                                                SequenceRemove,
                                                SequenceReverse,
                                                Sqrt,
                                                Sum
                                                ]

    @classmethod
    def interop_symbols(cls, package: str = None) -> Dict[str, IdentifiedSymbol]:
        return {symbol.raw_identifier if hasattr(symbol, 'raw_identifier') else symbol.identifier: symbol
                for symbol in Interop.interop_symbols(package)}

    # builtin decorator
    Metadata = MetadataDecorator()
    Public = PublicDecorator()

    # boa builtin type
    Event = EventType
    UInt160 = UInt160Type.build()
    UInt256 = UInt256Type.build()

    # boa events
    Nep5Transfer = Nep5TransferEvent()
    Nep17Transfer = Nep17TransferEvent()

    # boa smart contract methods
    Abort = AbortMethod()

    _boa_builtins: List[IdentifiedSymbol] = [Public,
                                             NewEvent,
                                             Event,
                                             Metadata,
                                             NeoMetadataType,
                                             ScriptHash
                                             ]

    metadata_fields: Dict[str, Union[type, Tuple[type]]] = {
        'author': (str, type(None)),
        'email': (str, type(None)),
        'description': (str, type(None)),
        'extras': dict
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
        BoaPackage.Contract: [Abort,
                              Nep17Transfer,
                              Nep5Transfer,
                              ],
        BoaPackage.Interop: Interop.package_symbols,
        BoaPackage.Type: [UInt160,
                          UInt256
                          ]
    }
