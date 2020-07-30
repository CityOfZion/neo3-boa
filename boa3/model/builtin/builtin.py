from typing import Dict, List, Optional, Tuple, Union

from boa3.model.builtin.classmethod.appendmethod import AppendMethod
from boa3.model.builtin.classmethod.clearmethod import ClearMethod
from boa3.model.builtin.classmethod.extendmethod import ExtendMethod
from boa3.model.builtin.classmethod.mapkeysmethod import MapKeysMethod
from boa3.model.builtin.classmethod.mapvaluesmethod import MapValuesMethod
from boa3.model.builtin.classmethod.reversemethod import ReverseMethod
from boa3.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.model.builtin.decorator.eventdecorator import EventDecorator
from boa3.model.builtin.decorator.metadatadecorator import MetadataDecorator
from boa3.model.builtin.decorator.publicdecorator import PublicDecorator
from boa3.model.builtin.interop.interop import Interop
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.builtin.method.bytearraymethod import ByteArrayMethod
from boa3.model.builtin.method.lenmethod import LenMethod
from boa3.model.builtin.neometadatatype import MetadataTypeSingleton as NeoMetadataType
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.method import Method
from boa3.model.type.itype import IType


class Builtin:
    @classmethod
    def get_symbol(cls, symbol_id: str) -> Optional[Method]:
        for name, method in vars(cls).items():
            if isinstance(method, IBuiltinDecorator) and method.identifier == symbol_id:
                return method

    @classmethod
    def get_by_self(cls, symbol_id: str, self_type: IType) -> Optional[Method]:
        for name, method in vars(cls).items():
            if (isinstance(method, IBuiltinMethod)
                    and method.identifier == symbol_id
                    and method.validate_self(self_type)):
                return method

    # builtin method
    Len = LenMethod()

    # python builtin class constructor
    ByteArray = ByteArrayMethod()

    # python class method
    SequenceAppend = AppendMethod()
    SequenceClear = ClearMethod()
    SequenceExtend = ExtendMethod()
    SequenceReverse = ReverseMethod()
    DictKeys = MapKeysMethod()
    DictValues = MapValuesMethod()

    _python_builtins: List[IdentifiedSymbol] = [Len,
                                                ByteArray,
                                                SequenceAppend,
                                                SequenceClear,
                                                SequenceExtend,
                                                SequenceReverse,
                                                DictKeys,
                                                DictValues]

    @classmethod
    def interop_symbols(cls, package: str = None) -> Dict[str, IdentifiedSymbol]:
        return {method.identifier: method for method in Interop.interop_symbols(package)}

    # builtin decorator
    Public = PublicDecorator()
    Event = EventDecorator()
    Metadata = MetadataDecorator()

    _boa_builtins: List[IdentifiedSymbol] = [Public,
                                             Event,
                                             Metadata,
                                             NeoMetadataType]

    @classmethod
    def boa_symbols(cls) -> Dict[str, IdentifiedSymbol]:
        return {symbol.identifier: symbol for symbol in cls._boa_builtins}

    metadata_fields: Dict[str, Union[type, Tuple[type]]] = \
        {
            'author': (str, type(None)),
            'email': (str, type(None)),
            'description': (str, type(None)),
            'has_storage': bool,
            'is_payable': bool
    }
