from boa3.builtin import NeoMetadata, metadata
from boa3.builtin.interop.storage import delete


def Main(key: bytes):
    delete(key)


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
