from boa3.builtin.compile_time import NeoMetadata, public


@public
def main() -> int:
    return 5


def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_permission(contract='*', methods=['*'])

    return meta
