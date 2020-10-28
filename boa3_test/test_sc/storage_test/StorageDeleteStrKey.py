from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop.storage import delete


@public
def Main(key: str):
    delete(key)


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
