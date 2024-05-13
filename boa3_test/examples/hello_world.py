from boa3.sc import storage
from boa3.sc.compiletime import NeoMetadata, public


@public
def Main():
    storage.put(b'hello', b'world')


def manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.author = "COZ in partnership with Simpli"
    meta.email = "contact@coz.io"
    meta.description = 'This is a contract example'
    return meta
