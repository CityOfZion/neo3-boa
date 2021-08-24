from boa3.builtin.nativecontract.contractmanagement import ContractManagement


def Main(script: bytes):
    ContractManagement.update(script)
