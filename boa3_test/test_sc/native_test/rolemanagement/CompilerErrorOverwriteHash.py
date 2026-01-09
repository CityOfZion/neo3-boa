from boa3.sc.contracts import RoleManagement
from boa3.sc.types import UInt160


def main() -> UInt160:
    RoleManagement.hash = UInt160()
    return RoleManagement.hash
