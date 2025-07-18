from boa3.sc.compiletime import public
from boa3.sc.types import ContractParameterType


@public
def main(x: ContractParameterType) -> int:
    return ~x
