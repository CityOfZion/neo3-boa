from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop import storage


@public
def Main():
    storage.put('hello', 'world')


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.author = "COZ in partnership with Simpli"
    meta.email = "contact@coz.io"
    meta.description = 'This is a contract example'
    return meta
