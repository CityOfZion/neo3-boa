from boa3.builtin.compile_time import public
from boa3.builtin.interop import role
from boa3.builtin.type import ECPoint


@public
def main(role_: role.Role, index: int) -> ECPoint:
    return role.get_designated_by_role(role_, index)
