from boa3.sc.contracts import RoleManagement
from boa3.sc.types import ECPoint, Role


def main(role: Role) -> ECPoint:
    return RoleManagement.get_designated_by_role(role)
