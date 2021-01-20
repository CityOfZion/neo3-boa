from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def extras_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.extras = {'unittest1': 'string',
                   'unittest2': 123,
                   'unittest3': True,
                   'unittest4': ['list', 3210]
                   }
    return meta
