from typing import Any

from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.contract import Nep17TransferEvent
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.interop.runtime import calling_script_hash, check_witness
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
    meta.author = "COZ"
    meta.description = "NEP-17 Example"
    meta.email = "contact@coz.io"
    return meta


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


# Script hash of the contract owner
OWNER = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
SUPPLY_KEY = 'totalSupply'

# Symbol of the Token
TOKEN_SYMBOL = 'NEP17'

# Number of decimal places
TOKEN_DECIMALS = 8

# Total Supply of tokens in the system
TOKEN_TOTAL_SUPPLY = 10_000_000 * 100_000_000  # 10m total supply * 10^8 (decimals)


# -------------------------------------------
# Events
# -------------------------------------------


on_transfer = Nep17TransferEvent


# -------------------------------------------
# Methods
# -------------------------------------------


@public
def symbol() -> str:
    """
    Gets the symbols of the token.

    This string must be valid ASCII, must not contain whitespace or control characters, should be limited to uppercase
    Latin alphabet (i.e. the 26 letters used in English) and should be short (3-8 characters is recommended).
    This method must always return the same value every time it is invoked.

    :return: a short string representing symbol of the token managed in this contract.
    """
    return TOKEN_SYMBOL


@public
def decimals() -> int:
    """
    Gets the amount of decimals used by the token.

    E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
    This method must always return the same value every time it is invoked.

    :return: the number of decimals used by the token.
    """
    return TOKEN_DECIMALS


@public
def totalSupply() -> int:
    """
    Gets the total token supply deployed in the system.

    This number must not be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
    must return 10,000,000 * 10 ^ decimals.

    :return: the total token supply deployed in the system.
    """
    return TOKEN_TOTAL_SUPPLY


@public
def balanceOf(account: UInt160) -> int:   # TODO: change bytes to hash160 when possible
    """
    Get the current balance of an address

    The parameter account must be a 20-byte address represented by a UInt160.

    :param account: the account address to retrieve the balance for
    :type account: bytes
    """
    return get(account.toBytes()).to_int()


@public
def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    """
    Transfers an amount of NEP17 tokens from one account to another

    If the method succeeds, it must fire the `transfer` event and must return true, even if the amount is 0,
    or from and to are the same address.

    :param from_address: the address to transfer from
    :type from_address: bytes
    :param to_address: the address to transfer to
    :type to_address: bytes
    :param amount: the amount of NEP5 tokens to transfer
    :type amount: int
    :param data: whatever data is pertinent to the onPayment method
    :type data: Any

    :return: whether the transfer was successful
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` if less than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(from_address) == 20 and len(to_address) == 20
    # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
    assert amount >= 0

    # The function MUST return false if the from account balance does not have enough tokens to spend.
    from_balance = get(from_address).to_int()
    if from_balance < amount:
        return False

    # The function should check whether the from address equals the caller contract hash.
    # If so, the transfer should be processed;
    # If not, the function should use the check_witness to verify the transfer.
    if from_address != calling_script_hash:
        if not check_witness(from_address):
            return False

    # if the `to_address` is a deployed contract, the function should check the payable flag of this contract
    # TODO: include example when objects are implemented

    if from_address == to_address:
        # transfer to self
        return True

    if from_balance == amount:
        delete(from_address)
    else:
        put(from_address, from_balance - amount)

    to_balance = get(to_address).to_int()
    put(to_address, to_balance + amount)

    # if the method succeeds, it must fire the transfer event
    on_transfer(from_address, to_address, amount)
    # if the to_address is a smart contract, it must call the contracts onPayment
    post_transfer(from_address, to_address, amount, data)
    # and then it must return true
    return True


def post_transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any):
    if to_address is not None:
        contract = get_contract(to_address)
        if(contract is not None):
            call_contract(to_address, 'onPayment', [from_address, amount, data])


@public
def verify() -> bool:
    """
    When this contract address is included in the transaction signature,
    this method will be triggered as a VerificationTrigger to verify that the signature is correct.
    For example, this method needs to be called when withdrawing token from the contract.

    :return: whether the transaction signature is correct
    """
    return check_witness(OWNER)


@public
def deploy() -> bool:
    """
    Initializes the storage when the smart contract is deployed.

    :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
    """
    if not check_witness(OWNER):
        return False

    if get(SUPPLY_KEY).to_int() > 0:
        return False

    put(SUPPLY_KEY, TOKEN_TOTAL_SUPPLY)
    put(OWNER, TOKEN_TOTAL_SUPPLY)

    on_transfer(b'', OWNER, TOKEN_TOTAL_SUPPLY)
    return True
