from enum import Enum

from boa3.internal.model.builtin.interop.interop import Interop
from boa3.internal.model.imports.package import Package


class BoaSCPackage(str, Enum):
    Storage = 'storage'
    Types = 'types'


class ContractImports:

    @classmethod
    def package_symbols(cls, package: str = None) -> Package | None:
        if package in BoaSCPackage.__members__.values():
            return cls._pkg_tree[package]

    StorageContextModule = Package(
        identifier=Interop.StorageContextType.identifier.lower(),
        types=[
            Interop.StorageContextType
        ]
    )

    StorageMapModule = Package(
        identifier=Interop.StorageMapType.identifier.lower(),
        types=[
            Interop.StorageMapType
        ]
    )

    StoragePackage = Package(
        identifier=BoaSCPackage.Storage,
        types=[
            Interop.StorageContextType,
            Interop.StorageMapType,
        ],
        methods=[
            Interop.StorageDelete,
            Interop.StorageFind,
            Interop.StorageGet,
            Interop.StorageGetInt,
            Interop.StorageGetBool,
            Interop.StorageGetStr,
            Interop.StorageGetUInt160,
            Interop.StorageGetUInt256,
            Interop.StorageGetECPoint,
            Interop.StorageGetContext,
            Interop.StorageGetCheck,
            Interop.StorageGetCheckInt,
            Interop.StorageGetCheckBool,
            Interop.StorageGetCheckStr,
            Interop.StorageGetCheckUInt160,
            Interop.StorageGetCheckUInt256,
            Interop.StorageGetCheckECPoint,
            Interop.StorageGetReadOnlyContext,
            Interop.StoragePut,
            Interop.StoragePutInt,
            Interop.StoragePutBool,
            Interop.StoragePutStr,
            Interop.StoragePutUInt160,
            Interop.StoragePutUInt256,
            Interop.StoragePutECPoint,
        ],
        packages=[
            Interop.FindOptionsModule,
            Interop.StorageContextModule,
            Interop.StorageMapModule
        ]
    )

    FindOptionsModule = Package(
        identifier=Interop.FindOptionsType.identifier.lower(),
        types=[
            Interop.FindOptionsType
        ]
    )

    TypesPackage = Package(
        identifier=BoaSCPackage.Types,
        types=[
            Interop.FindOptionsType,
        ],
        packages=[
            Interop.FindOptionsModule,
        ]
    )

    _pkg_tree: dict[BoaSCPackage, Package] = {
        pkg.identifier: pkg for pkg in [
            StoragePackage,
            TypesPackage,
        ]
    }
