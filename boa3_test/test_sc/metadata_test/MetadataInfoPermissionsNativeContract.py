from boa3.builtin.compile_time import NeoMetadata, public
from boa3.builtin.nativecontract.contractmanagement import ContractManagement


def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    # permission to call 'update' and 'destroy' from ContractManagement should be included by the compiler
    return meta


@public
def update(nef_file: bytes, manifest: bytes):
    ContractManagement.update(nef_file, manifest)


@public
def destroy():
    ContractManagement.destroy()
