from boa3.sc.contracts import ContractManagement


def Main(scripthash: bytes):
    ContractManagement.deploy(scripthash)
