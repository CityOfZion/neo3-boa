from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop.storage import get


@public
def Main(key: str) -> bytes:
    return get(key)


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
