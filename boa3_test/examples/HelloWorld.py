from boa3.builtin import metadata, NeoMetadata, public
from boa3.builtin.interop.storage import put


@public
def Main():
    put('hello', 'world')


@metadata
def manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.author = 'Neo'
    meta.email = 'dev@neo.org'
    meta.description = 'This is a contract example'
    meta.has_storage = True
    return meta
