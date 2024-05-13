from boa3.sc.compiletime import NeoMetadata, public


@public
def Main() -> int:
    return 5


def name_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.name = "SmartContractCustomName"

    return meta
