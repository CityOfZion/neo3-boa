from boa3.sc.contracts import ContractManagement


def Main(script: bytes):
    ContractManagement.update(script)
