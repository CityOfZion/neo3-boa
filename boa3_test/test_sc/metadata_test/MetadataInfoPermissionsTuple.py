from boa3.sc.compiletime import NeoMetadata, public


@public
def main() -> int:
    return 5


def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_permission(contract='*', methods=('total_supply', 'onNEP17Payment'))

    return meta
