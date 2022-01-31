from boa3.builtin import NeoMetadata, metadata


def Main() -> int:
    return 5


@metadata
def extras_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.unit_test1 = 'string'
    meta.unit_test2 = 123
    meta.unit_test3 = True
    meta.unit_test4 = ['list', 3210]

    return meta
