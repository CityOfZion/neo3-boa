from boa3.builtin import public
from boa3.builtin.nativecontract.contractmanagement import ContractManagement


@public
def Main():
    ContractManagement.destroy()
