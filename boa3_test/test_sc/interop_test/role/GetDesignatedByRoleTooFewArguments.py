from boa3.builtin.interop.role import Role, get_designated_by_role
from boa3.builtin.type import ECPoint


def main(role: Role) -> ECPoint:
    return get_designated_by_role(role)
