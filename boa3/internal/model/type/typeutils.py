from typing import Dict, List

from boa3.internal.model.callable import Callable
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.annotation.metatype import metaType
from boa3.internal.model.type.type import Type
from boa3.internal.model.type.typingmethod.casttypemethod import CastTypeMethod


class TypeUtils:
    @classmethod
    def all_functions(cls) -> Dict[str, Callable]:
        from boa3.internal.model.builtin.builtincallable import IBuiltinCallable
        return {tpe._identifier: tpe for tpe in vars(cls).values() if isinstance(tpe, IBuiltinCallable)}

    @classmethod
    def get_types_from_typing_lib(cls) -> Dict[str, ISymbol]:
        import typing
        from types import FunctionType

        type_symbols: Dict[str, ISymbol] = {}
        all_types: List[str] = typing.__all__

        for t_id in all_types:
            attr = getattr(typing, t_id)
            if not isinstance(attr, FunctionType):
                type_id: str = t_id if t_id in Type.all_types() else t_id.lower()
                if type_id in Type.all_types():
                    type_symbols[t_id] = Type.all_types()[type_id]
            else:
                function_id: str = t_id if t_id in cls.all_functions() else t_id.lower()
                if function_id in cls.all_functions():
                    type_symbols[t_id] = cls.all_functions()[function_id]

        return type_symbols

    # type for internal validation
    type = metaType

    # Annotation function utils
    cast = CastTypeMethod()

    _internal_validation_symbols: List[IdentifiedSymbol] = [type
                                                            ]

    symbols_for_internal_validation = {symbol.identifier: symbol
                                       for symbol in _internal_validation_symbols}
