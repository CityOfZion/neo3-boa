from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.contracts import ContractManagement


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
