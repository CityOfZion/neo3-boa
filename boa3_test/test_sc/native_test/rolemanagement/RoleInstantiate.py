from boa3.sc.compiletime import public
from boa3.sc.types import Role


@public
def main(x: int) -> Role:
    return Role(x)
