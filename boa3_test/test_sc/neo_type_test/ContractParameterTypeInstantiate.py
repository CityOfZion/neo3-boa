from boa3.sc.compiletime import public
from boa3.sc.types import ContractParameterType


@public
def main(x: int) -> ContractParameterType:
    return ContractParameterType(x)
