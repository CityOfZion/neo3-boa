from boa3.sc.compiletime import public
from boa3.sc.runtime import burn_gas


@public
def main(gas: int):
    burn_gas(gas)
