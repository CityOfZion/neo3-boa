from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160

current_height: int = 0


def get_contract(hash: UInt160) -> Contract:
    """
    Gets a contract with a given hash

    :param hash: a smart contract hash
    :type hash: UInt160
    :return: a contract
    :rtype: Contract
    :raise Exception: raised if hash length isn't 20 bytes
    """
    pass
