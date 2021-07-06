from boa3.builtin import public
from boa3.builtin.interop.role import get_designated_by_role, Role
from boa3.builtin.type import ECPoint


@public
def main() -> ECPoint:
    return get_designated_by_role(Role.STATE_VALIDATOR, 0)
