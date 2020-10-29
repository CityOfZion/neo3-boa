from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop.storage import put


@public
def Main(key: bytes):
    value: str = '123'
    put(key, value)


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
