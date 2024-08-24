__all__ = [
    'RoleManagement',
]

from boa3.sc.types import ECPoint, UInt160, Role


class RoleManagement:
    """
    A class used to represent the RoleManagement native contract.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/native/RoleManagement>`__
    to learn more about the RoleManagement class.
    """

    hash: UInt160

    @classmethod
    def get_designated_by_role(cls, role: Role, index: int) -> ECPoint:
        """
        Gets the list of nodes for the specified role.

        >>> RoleManagement.get_designated_by_role(Role.ORACLE, 0)
        []

        :param role: the type of the role
        :type role: boa3.sc.type.Role
        :param index: the index of the block to be queried
        :type index: int

        :return: the public keys of the nodes
        :rtype: boa3.sc.types.ECPoint
        """
        pass
