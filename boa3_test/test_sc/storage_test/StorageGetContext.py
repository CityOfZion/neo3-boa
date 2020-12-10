from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop.storage import get_context
from boa3.builtin.interop.storage.storagecontext import StorageContext


@public
def main() -> StorageContext:
    return get_context()


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.has_storage = True
    return meta
