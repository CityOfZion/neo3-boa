__all__ = [
    'Role',
    'get_designated_by_role',
]

from boa3.builtin.interop.role.roletype import Role
from boa3.builtin.type import ECPoint
from boa3.internal.deprecation import deprecated


@deprecated(details='This module is deprecated. Use :class:`RoleManagement` from :mod:`boa3.sc.contracts` instead')
def get_designated_by_role(role: Role, index: int) -> ECPoint:
    """
    Gets the list of nodes for the specified role.

    >>> get_designated_by_role(Role.ORACLE, 0)
    []

    :param role: the type of the role
    :type role: boa3.builtin.interop.role.roletype.Role
    :param index: the index of the block to be queried
    :type index: int

    :return: the public keys of the nodes
    :rtype: boa3.builtin.type.ECPoint
    """
    pass
