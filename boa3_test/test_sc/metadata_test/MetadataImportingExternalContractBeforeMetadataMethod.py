from boa3.builtin.compile_time import NeoMetadata, public
from boa3_test.test_sc.metadata_test.aux_package.internal_package.external_contract import ExternalContract


def standards_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.description = 'Test importing a external contract before declaring the metadata'
    return meta


@public
def main() -> str:
    return ExternalContract.another_method()
