import enum

from boa3.internal.model.callable import Callable
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.imports.package import Package
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.annotation.metatype import metaType
from boa3.internal.model.type.type import Type
from boa3.internal.model.type.typingmethod.casttypemethod import CastTypeMethod


class TypingPackage(str, enum.Enum):
    Collections = 'collections'
    Typing = 'typing'


class TypeUtils:
    @classmethod
    def all_functions(cls) -> dict[str, Callable]:
        from boa3.internal.model.builtin.builtincallable import IBuiltinCallable
        return {tpe._identifier: tpe for tpe in vars(cls).values() if isinstance(tpe, IBuiltinCallable)}

    @classmethod
    def package_symbols(cls, package: str = None) -> Package | None:
        if package in TypingPackage.__members__.values():
            if TypingPackage.Typing not in cls._pkg_tree:
                cls._pkg_tree[TypingPackage.Typing] = Package(
                    identifier=TypingPackage.Typing,
                    other_symbols=cls.get_types_from_typing_lib()
                )
            return cls._pkg_tree[package]

    @classmethod
    def get_types_from_typing_lib(cls) -> dict[str, ISymbol]:
        import typing
        from types import FunctionType

        type_symbols: dict[str, ISymbol] = {}
        all_types: list[str] = typing.__all__

        deprecated_builtins = [
            'List', 'Dict', 'Tuple'
        ]
        deprecated_collections = list(cls._pkg_tree[TypingPackage.Collections].inner_packages['abc'].symbols)

        for t_id in all_types:
            attr = getattr(typing, t_id)
            type_symbol = None
            if not isinstance(attr, FunctionType):
                type_id: str = t_id if t_id in Type.all_types() else t_id.lower()
                if type_id in Type.all_types():
                    type_symbol = Type.all_types()[type_id]
            else:
                function_id: str = t_id if t_id in cls.all_functions() else t_id.lower()
                if function_id in cls.all_functions():
                    type_symbol = cls.all_functions()[function_id]

            if isinstance(type_symbol, ISymbol):
                if t_id in deprecated_builtins:
                    type_symbol = type_symbol.clone()
                    type_symbol.deprecate(t_id.lower())
                elif t_id in deprecated_collections:
                    type_symbol = type_symbol.clone()
                    type_symbol.deprecate(f'{TypingPackage.Collections.value}.abc.{t_id}')

                type_symbols[t_id] = type_symbol

        return type_symbols

    # type for internal validation
    type = metaType

    # Annotation function utils
    cast = CastTypeMethod()

    _internal_validation_symbols: list[IdentifiedSymbol] = [type
                                                            ]

    symbols_for_internal_validation = {symbol.identifier: symbol
                                       for symbol in _internal_validation_symbols}

    _pkg_tree: dict[TypingPackage, Package] = {
        TypingPackage.Collections: Package.create_package(
            package_id=f'{TypingPackage.Collections.value}.abc',
            symbols={
                'Collection': Type.collection,
                'Mapping': Type.mapping,
                'MutableSequence': Type.mutableSequence,
                'Sequence': Type.sequence,
            }
        )
    }
