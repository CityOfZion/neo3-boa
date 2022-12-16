# -------------------------------------------
# This standard is deprecated
# Please check the NEP17 example
# -------------------------------------------

from typing import Any

from boa3.builtin.compile_time import NeoMetadata, metadata, public
from boa3.builtin.contract import Nep5TransferEvent
from boa3.builtin.interop import runtime, storage
from boa3.builtin.type import UInt160


# -------------------------------------------
# METADATA
# -------------------------------------------


@metadata
def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-5']

    meta.author = "Mirella Medeiros and Ricardo Prado. COZ in partnership with Simpli"
    meta.description = "NEP-5 Example"
    meta.email = "contact@coz.io"
    return meta


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


# Script hash of the contract owner
OWNER = UInt160(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
SUPPLY_KEY = 'totalSupply'

# Name of the Token
TOKEN_NAME = 'NEP5 Standard'

# Symbol of the Token
TOKEN_SYMBOL = 'NEP5'

# Number of decimal places
TOKEN_DECIMALS = 8

# Total Supply of tokens in the system
TOKEN_TOTAL_SUPPLY = 10_000_000 * 10 ** TOKEN_DECIMALS  # 10m total supply * 10^8 (decimals)

# -------------------------------------------
# Events
# -------------------------------------------


on_transfer = Nep5TransferEvent


# -------------------------------------------
# Methods
# -------------------------------------------


@public
def verify() -> bool:
    """
    When this contract address is included in the transaction signature,
    this method will be triggered as a VerificationTrigger to verify that the signature is correct.
    For example, this method needs to be called when withdrawing token from the contract.

    :return: whether the transaction signature is correct
    """
    return runtime.check_witness(OWNER)


@public
def name() -> str:
    """
    Gets the name of the token.

    This method must always return the same value every time it is invoked.

    :return: the name of the token.
    """
    return TOKEN_NAME


@public
def symbol() -> str:
    """
    Gets the symbols of the token.

    This symbol should be short (3-8 characters is recommended), with no whitespace characters or new-lines and should
    be limited to the uppercase latin alphabet (i.e. the 26 letters used in English).
    This method must always return the same value every time it is invoked.

    :return: a short string symbol of the token managed in this contract.
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

    This number mustn't be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
    must return 10,000,000 * 10 ^ decimals.

    :return: the total token supply deployed in the system.
    """
    return TOKEN_TOTAL_SUPPLY


@public
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
    return storage.get(account).to_int()


@public
def transfer(from_address: UInt160, to_address: UInt160, amount: int) -> bool:
    """
    Transfers a specified amount of NEP5 tokens from one account to another

    If the method succeeds, it must fire the `transfer` event and must return true, even if the amount is 0,
    or from and to are the same address.

    :param from_address: the address to transfer from
    :type from_address: UInt160
    :param to_address: the address to transfer to
    :type to_address: UInt160
    :param amount: the amount of NEP5 tokens to transfer
    :type amount: int

    :return: whether the transfer was successful
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` is less than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(from_address) == 20 and len(to_address) == 20
    # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
    assert amount >= 0

    # The function MUST return false if the from account balance does not have enough tokens to spend.
    from_balance = storage.get(from_address).to_int()
    if from_balance < amount:
        return False

    # The function should check whether the from address equals the caller contract hash.
    # If so, the transfer should be processed;
    # If not, the function should use the check_witness to verify the transfer.
    if from_address != runtime.calling_script_hash:
        if not runtime.check_witness(from_address):
            return False

    # if the `to_address` is a deployed contract, the function should check the payable flag of this contract
    # TODO: include example when objects are implemented

    if from_address == to_address:
        # transfer to self
        return True

    if from_balance == amount:
        storage.delete(from_address)
    else:
        storage.put(from_address, from_balance - amount)

    to_balance = storage.get(to_address).to_int()
    storage.put(to_address, to_balance + amount)

    # if the method succeeds, it must fire the transfer event, and must return true
    on_transfer(from_address, to_address, amount)
    return True


@public
def _deploy(data: Any, update: bool):
    """
    Initializes the storage when the smart contract is deployed.

    :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
    """
    if not update:
        storage.put(SUPPLY_KEY, TOKEN_TOTAL_SUPPLY)
        storage.put(OWNER, TOKEN_TOTAL_SUPPLY)

        on_transfer(b'', OWNER, TOKEN_TOTAL_SUPPLY)
