from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import burn_gas


@public
def main(gas: int):
    burn_gas(gas)
