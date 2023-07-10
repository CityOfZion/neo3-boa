__all__ = [
    'Role',
    'get_designated_by_role',
]


from boa3.builtin.interop.role.roletype import Role
from boa3.builtin.type import ECPoint


def get_designated_by_role(role: Role, index: int) -> ECPoint:
    """
    Gets the list of nodes for the specified role.

    >>> get_designated_by_role(Role.ORACLE, 0)
    []

    :param role: the type of the role
    :type role: Role
    :param index: the index of the block to be queried
    :type index: int

    :return: the public keys of the nodes
    :rtype: ECPoint
    """
    pass
