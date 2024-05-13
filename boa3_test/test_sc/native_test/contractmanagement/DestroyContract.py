from boa3.sc.compiletime import public
from boa3.sc.contracts import ContractManagement


@public
def Main():
    ContractManagement.destroy()
