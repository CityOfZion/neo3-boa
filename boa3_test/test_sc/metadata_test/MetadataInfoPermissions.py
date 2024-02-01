from boa3.builtin.compile_time import NeoMetadata, public


@public
def Main() -> int:
    return 5


def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    # the contract needs permission to call this method from any contract
    meta.add_permission(methods=['onNEP17Payment'])

    # the contract needs permission to call this method from a specific contract
    meta.add_permission(contract='0x3846a4aa420d9831044396dd3a56011514cd10e3', methods=['get_object'])

    # the contract needs permission to call any methods from any contract in this group
    meta.add_permission(contract='0333b24ee50a488caa5deec7e021ff515f57b7993b93b45d7df901e23ee3004916')

    return meta
