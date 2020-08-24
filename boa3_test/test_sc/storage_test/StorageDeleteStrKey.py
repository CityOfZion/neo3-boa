from boa3.builtin import metadata, NeoMetadata
from boa3.builtin.interop.storage import delete


def Main(key: str):
    delete(key)


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
