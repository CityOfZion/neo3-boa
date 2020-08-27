from boa3.builtin import metadata, NeoMetadata
from boa3.builtin.interop.storage import put


def Main(key: bytes):
    value: int = 123
    put(key, value)


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
