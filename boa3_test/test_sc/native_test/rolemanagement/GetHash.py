from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.rolemanagement import RoleManagement
from boa3.builtin.type import UInt160


@public
def main() -> UInt160:
    return RoleManagement.hash
