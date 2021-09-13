from boa3.builtin.interop.role import Role, get_designated_by_role
from boa3.builtin.type import ECPoint


def main(role: Role, index: int) -> ECPoint:
    return get_designated_by_role(role, index, 'arg')
