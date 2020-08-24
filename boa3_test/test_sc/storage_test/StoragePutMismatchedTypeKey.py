from boa3.builtin import metadata, NeoMetadata
from boa3.builtin.interop.storage import put


def Main(key: list):
    value: bytes = b'\x01\x02\x03'
    put(key, value)


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
