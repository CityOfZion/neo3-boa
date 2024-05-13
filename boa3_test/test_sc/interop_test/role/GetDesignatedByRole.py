from boa3.sc.compiletime import public
from boa3.sc.contracts import RoleManagement
from boa3.sc.types import ECPoint, Role


@public
def main(role: Role, index: int) -> ECPoint:
    return RoleManagement.get_designated_by_role(role, index)
