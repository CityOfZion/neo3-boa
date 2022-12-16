from boa3.builtin import interop
from boa3.builtin.compile_time import public
from boa3.builtin.type import ECPoint


@public
def main(role: interop.role.Role, index: int) -> ECPoint:
    return interop.role.get_designated_by_role(role, index)
