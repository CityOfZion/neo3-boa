from boa3.builtin import NeoMetadata, metadata
from boa3.builtin.interop.storage import put


def Main(key: bytes):
    value: list = [1, 2, 3]
    put(key, value)


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
