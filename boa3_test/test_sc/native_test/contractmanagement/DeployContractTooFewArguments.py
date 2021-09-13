from boa3.builtin.nativecontract.contractmanagement import ContractManagement


def Main(scripthash: bytes):
    ContractManagement.deploy(scripthash)
