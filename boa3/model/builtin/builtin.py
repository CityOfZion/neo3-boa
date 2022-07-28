from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from boa3.model.builtin.builtincallable import IBuiltinCallable
from boa3.model.builtin.classmethod import *
from boa3.model.builtin.contract import *
from boa3.model.builtin.decorator import *
from boa3.model.builtin.internal.innerdeploymethod import InnerDeployMethod
from boa3.model.builtin.interop.interop import Interop
from boa3.model.builtin.math import *
from boa3.model.builtin.method import *
from boa3.model.builtin.neometadatatype import MetadataTypeSingleton as NeoMetadataType
from boa3.model.callable import Callable
from boa3.model.event import Event as EventSymbol
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.imports.package import Package
from boa3.model.type.collection.sequence.ecpointtype import ECPointType
from boa3.model.type.collection.sequence.uint160type import UInt160Type
from boa3.model.type.collection.sequence.uint256type import UInt256Type
from boa3.model.type.itype import IType
from boa3.model.type.math import Math
from boa3.model.type.primitive.bytestringtype import ByteStringType


class BoaPackage(str, Enum):
    Contract = 'contract'
    Interop = 'interop'
    Type = 'type'


class Builtin:
    @classmethod
    def get_symbol(cls, symbol_id: str) -> Optional[Callable]:
        for method in cls._python_builtins:
            if isinstance(method, IBuiltinCallable) and method.identifier == symbol_id:
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
    Max = MaxIntMethod()
    Min = MinIntMethod()
    Print = PrintMethod()
    ScriptHash = ScriptHashMethod()
    StrSplit = StrSplitMethod()
    Sum = SumMethod()

    # python builtin class constructor
    Bool = BoolMethod()
    ByteArray = ByteArrayMethod()
    ByteArrayEncoding = ByteArrayEncodingMethod()
    Exception = ExceptionMethod()
    IntByteString = IntByteStringMethod()
    IntInt = IntIntMethod()
    ListBytesString = ListBytesStringMethod()
    ListGeneric = ListGenericMethod()
    ListMapping = ListMappingMethod()
    ListSequence = ListSequenceMethod()
    Range = RangeMethod()
    Reversed = ReversedMethod()
    Super = SuperMethod()

    # python class method
    BytesStringIndex = IndexBytesStringMethod()
    BytesStringIsDigit = IsDigitMethod()
    BytesStringJoin = JoinMethod()
    BytesStringLower = LowerMethod()
    BytesStringStartswith = StartsWithMethod()
    BytesStringStrip = StripMethod()
    BytesStringUpper = UpperMethod()
    CountSequenceGeneric = CountSequenceGenericMethod()
    CountSequencePrimitive = CountSequencePrimitiveMethod()
    CountStr = CountStrMethod()
    Copy = CopyListMethod()
    SequenceAppend = AppendMethod()
    SequenceClear = ClearMethod()
    SequenceExtend = ExtendMethod()
    SequenceIndex = IndexSequenceMethod()
    SequenceInsert = InsertMethod()
    SequencePop = PopSequenceMethod()
    SequenceRemove = RemoveMethod()
    SequenceReverse = ReverseMethod()
    DictKeys = MapKeysMethod()
    DictPop = PopDictMethod()
    DictPopDefault = PopDictDefaultMethod()
    DictValues = MapValuesMethod()

    # custom class methods
    ConvertToBytes = ToBytesMethod
    ConvertToInt = ToIntMethod
    ConvertToStr = ToStrMethod
    ConvertToBool = ToBoolMethod

    # builtin decorator
    ClassMethodDecorator = ClassMethodDecorator()
    InstanceMethodDecorator = InstanceMethodDecorator()
    PropertyDecorator = PropertyDecorator()
    StaticMethodDecorator = StaticMethodDecorator()

    _python_builtins: List[IdentifiedSymbol] = [Abs,
                                                ByteArray,
                                                ByteArrayEncoding,
                                                BytesStringIndex,
                                                BytesStringIsDigit,
                                                BytesStringJoin,
                                                BytesStringLower,
                                                BytesStringStartswith,
                                                BytesStringStrip,
                                                BytesStringUpper,
                                                ClassMethodDecorator,
                                                ConvertToBool,
                                                ConvertToBytes,
                                                ConvertToInt,
                                                ConvertToStr,
                                                Copy,
                                                CountSequenceGeneric,
                                                CountSequencePrimitive,
                                                CountStr,
                                                DictKeys,
                                                DictValues,
                                                Exception,
                                                Exit,
                                                IsInstance,
                                                Len,
                                                Max,
                                                Min,
                                                Print,
                                                PropertyDecorator,
                                                Range,
                                                Reversed,
                                                ScriptHash,
                                                SequenceAppend,
                                                SequenceClear,
                                                SequenceExtend,
                                                SequenceIndex,
                                                SequenceInsert,
                                                SequencePop,
                                                SequenceRemove,
                                                SequenceReverse,
                                                StaticMethodDecorator,
                                                StrSplit,
                                                Sum,
                                                Super,
                                                ]

    @classmethod
    def interop_symbols(cls, package: str = None) -> Dict[str, IdentifiedSymbol]:
        return {symbol.raw_identifier if hasattr(symbol, 'raw_identifier') else symbol.identifier: symbol
                for symbol in Interop.interop_symbols(package)}

    # boa builtin decorator
    ContractInterface = ContractDecorator()
    ContractMethodDisplayName = DisplayNameDecorator()
    Metadata = MetadataDecorator()
    Public = PublicDecorator()

    # boa builtin type
    ByteString = ByteStringType.build()
    Event = EventType
    UInt160 = UInt160Type.build()
    UInt256 = UInt256Type.build()
    ECPoint = ECPointType.build()
    NeoAccountState = NeoAccountStateType.build()

    # boa events
    Nep5Transfer = Nep5TransferEvent()
    Nep11Transfer = Nep11TransferEvent()
    Nep17Transfer = Nep17TransferEvent()

    # boa smart contract methods
    Abort = AbortMethod()

    # region boa builtin modules

    BuiltinMathCeil = DecimalCeilingMethod()
    BuiltinMathFloor = DecimalFloorMethod()

    MathModule = Package(identifier='math',
                         methods=[Math.Sqrt,
                                  BuiltinMathCeil,
                                  BuiltinMathFloor])

    _modules = [MathModule]

    # endregion

    boa_builtins: List[IdentifiedSymbol] = [ContractInterface,
                                            ContractMethodDisplayName,
                                            Event,
                                            Metadata,
                                            NeoMetadataType,
                                            NewEvent,
                                            Public,
                                            ScriptHash
                                            ] + _modules

    metadata_fields: Dict[str, Union[type, Tuple[type]]] = {
        'name': str,
        'supported_standards': list,
        'trusts': list,
        'author': (str, type(None)),
        'email': (str, type(None)),
        'description': (str, type(None)),
        'extras': dict
    }

    @classmethod
    def boa_symbols(cls) -> Dict[str, IdentifiedSymbol]:
        return {symbol.identifier: symbol for symbol in cls.boa_builtins}

    @classmethod
    def package_symbols(cls, package: str = None) -> Dict[str, IdentifiedSymbol]:
        if package in BoaPackage.__members__.values():
            return {symbol.identifier: symbol for symbol in cls._boa_symbols[package]}

        return cls.boa_symbols()

    @classmethod
    def builtin_events(cls) -> List[EventSymbol]:
        lst: List[EventSymbol] = [event for event in cls.boa_builtins if isinstance(event, EventSymbol)]

        for symbols in cls._boa_symbols.values():
            lst.extend([event for event in symbols if isinstance(event, EventSymbol)])

        return lst

    _boa_symbols: Dict[BoaPackage, List[IdentifiedSymbol]] = {
        BoaPackage.Contract: [Abort,
                              NeoAccountState,
                              Nep11Transfer,
                              Nep17Transfer,
                              Nep5Transfer,
                              ],
        BoaPackage.Interop: Interop.package_symbols,
        BoaPackage.Type: [ByteString,
                          ECPoint,
                          UInt160,
                          UInt256
                          ]
    }

    _internal_methods = [InnerDeployMethod.instance()
                         ]
    internal_methods = {method.raw_identifier: method for method in _internal_methods}
