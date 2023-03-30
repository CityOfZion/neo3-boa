from enum import IntFlag


class Role(IntFlag):
    """
    Represents the roles in the NEO system. They are the permission types of the native contract `RoleManagement`.
    """

    STATE_VALIDATOR = 4
    """
    The validators of state. Used to generate and sign the state root.

    :meta hide-value:
    """

    ORACLE = 8
    """
    The nodes used to process Oracle requests.

    :meta hide-value:
    """

    NEO_FS_ALPHABET_NODE = 16
    """
    NeoFS Alphabet nodes.

    :meta hide-value:
    """
