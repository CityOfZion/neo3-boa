from boa3.builtin import NeoMetadata, metadata
from boa3.builtin.interop.storage import get


def Main(key: int) -> bytes:
    return get(key)


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
