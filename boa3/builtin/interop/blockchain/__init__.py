from boa3.builtin.interop.contract import Contract

current_height: int = 0


def get_contract(hash: bytes) -> Contract:  # TODO: Change bytes to Hash160 when implemented
    """
    Gets a contract with a given hash

    :param hash: a smart contract hash
    :type hash: bytes
    :return: a contract
    :rtype: Contract
    :raise Exception: raised if hash length isn't 20 bytes
    """
    pass
