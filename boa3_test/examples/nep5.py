from boa3.builtin import event, metadata, NeoMetadata
from boa3.builtin.interop.runtime import check_witness
from boa3.builtin.interop.storage import delete, get, put


# -------------------------------------------
# METADATA
# -------------------------------------------


@metadata
def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.has_storage = True
    meta.is_payable = True
    return meta


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


# Script hash of the contract owner
OWNER = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

# Name of the Token
TOKEN_NAME = 'NEP5 Standard'

# Symbol of the Token
TOKEN_SYMBOL = 'NEP5'

# Number of decimal places
TOKEN_DECIMALS = 8

# Total Supply of tokens in the system
TOKEN_TOTAL_SUPPLY = 10_000_000 * 100_000_000  # 10m total supply * 10^8 (decimals)


# -------------------------------------------
# Events
# -------------------------------------------


@event
def on_transfer(from_addr: bytes, to_addr: bytes, amount: int):
    """
    Triggers the `transfer` event

    Must be triggered when tokens are transferred, including zero value transfers.

    :param from_addr: the address to transfer from
    :type from_addr: bytes
    :param to_addr: the address to transfer to
    :type to_addr: bytes
    :param amount: the amount of NEP5 tokens to transfer
    :type amount: int
    """
    pass


# -------------------------------------------
# Methods
# -------------------------------------------


def verify() -> bool:
    """
    When this contract address is included in the transaction signature,
    this method will be triggered as a VerificationTrigger to verify that the signature is correct.
    For example, this method needs to be called when withdrawing token from the contract.

    :return: whether the transaction signature is correct
    """
    return check_witness(OWNER)


def name() -> str:
    """
    Gets the name of the token.

    This method must always return the same value every time it is invoked.

    :return: the name of the token.
    """
    return TOKEN_NAME


def symbol() -> str:
    """
    Gets the symbols of the token.

    This symbol should be short (3-8 characters is recommended), with no whitespace characters or new-lines and should
    be limited to the uppercase latin alphabet (i.e. the 26 letters used in English).
    This method must always return the same value every time it is invoked.

    :return: a short string symbol of the token managed in this contract.
    """
    return TOKEN_SYMBOL


def decimals() -> int:
    """
    Gets the amount of decimals used by the token.

    E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
    This method must always return the same value every time it is invoked.

    :return: the number of decimals used by the token.
    """
    return TOKEN_DECIMALS


def totalSupply() -> int:
    """
    Gets the total token supply deployed in the system.

    This number mustn't be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
    must return 10,000,000 * 10 ^ decimals.

    :return: the total token supply deployed in the system.
    """
    return TOKEN_TOTAL_SUPPLY


def balanceOf(account: bytes) -> int:
    """
    Get the current balance of an address

    The parameter account should be a 20-byte address.

    :param account: the account address to retrieve the balance for
    :type account: bytes

    :return: the token balance of the `account`
    :raise AssertionError: raised if `account` length is not 20.
    """
    assert len(account) == 20
    return int(get(account))


def transfer(from_addr: bytes, to_addr: bytes, amount: int) -> bool:
    """
    Transfers a specified amount of NEP5 tokens from one account to another

    If the method succeeds, it must fire the `transfer` event and must return true, even if the amount is 0,
    or from and to are the same address.

    :param from_addr: the address to transfer from
    :type from_addr: bytes
    :param to_addr: the address to transfer to
    :type to_addr: bytes
    :param amount: the amount of NEP5 tokens to transfer
    :type amount: int

    :return: whether the transfer was successful
    :raise AssertionError: raised if `from_addr` or `to_addr` length is not 20 or if `amount` if less than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(from_addr) == 20 and len(to_addr) == 20
    # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
    assert amount >= 0

    # The function MUST return false if the from account balance does not have enough tokens to spend.
    from_balance = int(get(from_addr))
    if from_balance < amount:
        return False
    # check if from is the same script hash of the caller
    # if not:
    if not check_witness(from_addr):
        return False

    # if the `to_addr` is a deployed contract, the function should check the payable flag of this contract

    if from_addr == to_addr:
        # transfer to self
        return True

    if from_balance == amount:
        delete(from_addr)
    else:
        put(from_addr, from_balance - amount)

    to_balance = int(get(to_addr))
    put(to_addr, to_balance + amount)

    # if the method succeeds, it must fire the transfer event, and must return true
    on_transfer(from_addr, to_addr, amount)
    return True
