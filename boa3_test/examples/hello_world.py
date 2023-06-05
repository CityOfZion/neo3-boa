from boa3.builtin.compile_time import NeoMetadata, metadata, public
from boa3.builtin.interop import storage


@public
def Main():
    storage.put(b'hello', b'world')


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.author = "COZ in partnership with Simpli"
    meta.email = "contact@coz.io"
    meta.description = 'This is a contract example'
    return meta
