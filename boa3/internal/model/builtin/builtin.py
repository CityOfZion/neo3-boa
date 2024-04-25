from enum import Enum

from boa3.internal.model.builtin.builtincallable import IBuiltinCallable
from boa3.internal.model.builtin.classmethod import *
from boa3.internal.model.builtin.compile_time import *
from boa3.internal.model.builtin.contract import *
from boa3.internal.model.builtin.decorator import *
from boa3.internal.model.builtin.internal import *
from boa3.internal.model.builtin.interop.interop import Interop
from boa3.internal.model.builtin.math import *
from boa3.internal.model.builtin.method import *
from boa3.internal.model.callable import Callable
from boa3.internal.model.event import Event as EventSymbol
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.imports.package import Package
from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.math import Math
from boa3.internal.model.type.neo import *


class BoaPackage(str, Enum):
    CompileTime = 'compile_time'
    Contract = 'contract'
    Interop = 'interop'
    Type = 'type'
    TypeHelper = 'helper'
    VM = 'vm'


class Builtin:
    @classmethod
    def get_symbol(cls, symbol_id: str) -> Callable | None:
        for method in cls._python_builtins:
            if isinstance(method, IBuiltinCallable) and method.identifier == symbol_id:
                return method

    @classmethod
    def get_by_self(cls, symbol_id: str, self_type: IType) -> Callable | None:
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
    ScriptHashMethod_ = ScriptHashMethod()
    StrSplit = StrSplitMethod()
    Sum = SumMethod()
    ToHexStr = ToHexStrMethod()

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
    StrBool = StrBoolMethod()
    StrBytes = StrBytesMethod()
    StrClass = StrClassMethod()
    StrInt = StrIntMethod()
    StrSequence = StrSequenceMethod()
    Super = SuperMethod()

    # python class method
    BytesStringIndex = IndexBytesStringMethod()
    BytesStringIsDigit = IsDigitMethod()
    BytesStringJoin = JoinMethod()
    BytesStringLower = LowerMethod()
    BytesStringStartswith = StartsWithMethod()
    BytesStringStrip = StripMethod()
    BytesStringUpper = UpperMethod()
    BytesStringReplace = ReplaceMethod()
    CountSequenceGeneric = CountSequenceGenericMethod()
    CountSequencePrimitive = CountSequencePrimitiveMethod()
    CountStr = CountStrMethod()
    Copy = CopyListMethod()
    ListSort = SortMethod()
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

    _python_builtins: list[IdentifiedSymbol] = [
        Abs,
        ByteArray,
        ByteArrayEncoding,
        BytesStringIndex,
        BytesStringIsDigit,
        BytesStringJoin,
        BytesStringLower,
        BytesStringStartswith,
        BytesStringStrip,
        BytesStringUpper,
        BytesStringReplace,
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
        ListSort,
        Max,
        Min,
        Print,
        PropertyDecorator,
        Range,
        Reversed,
        ScriptHashMethod_,
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

    # boa builtin decorator
    ContractInterface = ContractDecorator()
    ContractMethodDisplayName = DisplayNameDecorator()
    Public = PublicDecorator()

    # boa builtin type
    Event = EventType
    UInt160 = UInt160Type.build()
    UInt256 = UInt256Type.build()
    ECPoint = ECPointType.build()
    NeoAccountState = NeoAccountStateType.build()
    Opcode = OpcodeType.build()
    Address = AddressType.build()
    BlockHash = BlockHashType.build()
    PublicKey = PublicKeyType.build()
    ScriptHashType_ = ScriptHashType.build()
    ScriptHashLittleEndian = ScriptHashLittleEndianType.build()
    TransactionId = TransactionIdType.build()

    # boa events
    Nep11Transfer = Nep11TransferEvent()
    Nep17Transfer = Nep17TransferEvent()

    # boa contract interfaces
    Nep17Contract = Nep17ContractClass()

    # boa smart contract methods
    Abort = AbortMethod()
    Env = EnvProperty.build()

    # region boa builtin modules

    BuiltinMathCeil = DecimalCeilingMethod()
    BuiltinMathFloor = DecimalFloorMethod()

    MathModule = Package(identifier='math',
                         methods=[Math.Sqrt,
                                  BuiltinMathCeil,
                                  BuiltinMathFloor])

    _symbols = [Env]
    _modules = [MathModule]

    # endregion

    boa_builtins: list[IdentifiedSymbol] = []
    boa_builtins.extend(_modules)
    boa_builtins.extend(_symbols)

    metadata_fields: dict[str, type | tuple[type, ...]] = {
        'name': str,
        'source': (str, type(None)),
        'supported_standards': list,
        'trusts': list,
        'author': (str, type(None)),
        'email': (str, type(None)),
        'description': (str, type(None)),
        'extras': dict
    }

    @classmethod
    def boa_symbols(cls) -> dict[str, IdentifiedSymbol]:
        return {symbol.identifier: symbol for symbol in cls.boa_builtins}

    @classmethod
    def package_symbols(cls, package: str = None) -> dict[str, IdentifiedSymbol]:
        if package in BoaPackage.__members__.values():
            return {symbol.identifier: symbol for symbol in cls._boa_symbols[package]}

        return cls.boa_symbols()

    @classmethod
    def builtin_events(cls) -> list[EventSymbol]:
        lst: list[EventSymbol] = [event for event in cls.boa_builtins if isinstance(event, EventSymbol)]

        for symbols in cls._boa_symbols.values():
            lst.extend([event for event in symbols if isinstance(event, EventSymbol)])

        return lst

    _builtin_type_package_symbols = [ECPoint,
                                     UInt160,
                                     UInt256,
                                     Event,
                                     Address,
                                     BlockHash,
                                     PublicKey,
                                     ScriptHashType_,
                                     ScriptHashLittleEndian,
                                     TransactionId,
                                     Package(identifier=BoaPackage.TypeHelper,
                                             methods=[ConvertToBool,
                                                      ConvertToBytes,
                                                      ConvertToInt,
                                                      ConvertToStr,
                                                      ]
                                             )
                                     ]

    _boa_symbols: dict[BoaPackage, list[IdentifiedSymbol]] = {
        BoaPackage.Contract: [Abort,
                              NeoAccountState,
                              Nep11Transfer,
                              Nep17Transfer,
                              Nep17Contract,
                              ScriptHashMethod_,
                              ToHexStr,
                              ],
        BoaPackage.Interop: Interop.package_symbols,
        BoaPackage.Type: _builtin_type_package_symbols,
        BoaPackage.VM: [Opcode
                        ],
        BoaPackage.CompileTime: [ContractInterface,
                                 ContractMethodDisplayName,
                                 NeoMetadataType,
                                 Public,
                                 NewEvent
                                 ]
    }

    _internal_methods = [InnerDeployMethod.instance()
                         ]
    internal_methods = {method.raw_identifier: method for method in _internal_methods}
