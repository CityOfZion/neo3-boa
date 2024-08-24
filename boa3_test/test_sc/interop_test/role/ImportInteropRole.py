from boa3.builtin import interop
from boa3.sc.compiletime import public
from boa3.sc.types import ECPoint


@public
def main(role: interop.role.Role, index: int) -> ECPoint:
    return interop.role.get_designated_by_role(role, index)
