from boa3.sc.compiletime import public
from boa3.sc.types import FindOptions


@public
def main(option1: FindOptions, option2: FindOptions) -> int:
    return option1 % option2
