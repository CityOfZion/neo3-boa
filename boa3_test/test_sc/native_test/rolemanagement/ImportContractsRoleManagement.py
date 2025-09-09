from boa3.sc import contracts
from boa3.sc.compiletime import public
from boa3.sc.types import ECPoint, Role


@public
def main(role_: Role, index: int) -> ECPoint:
    return contracts.RoleManagement.get_designated_by_role(role_, index)
