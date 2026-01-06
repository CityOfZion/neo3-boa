from boa3.sc.compiletime import public
from boa3.sc.contracts import RoleManagement
from boa3.sc.types import ECPoint, Role


@public
def main(role: Role, nodes: list[ECPoint]):
    RoleManagement.designate_as_role(role, nodes)
