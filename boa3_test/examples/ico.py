from typing import List

from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.contract import Nep5TransferEvent
from boa3.builtin.interop.contract import GAS, NEO, call_contract
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
    meta.has_storage = True
    meta.is_payable = True
    return meta


# -------------------------------------------
# Storage Key Prefixes
# -------------------------------------------


KYC_WHITELIST_PREFIX = b'KYCWhitelistApproved'
TOKEN_TOTAL_SUPPLY_PREFIX = b'TokenTotalSupply'
TRANSFER_ALLOWANCE_PREFIX = b'TransferAllowancePrefix_'


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


# Script hash of the contract owner
TOKEN_OWNER = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

# Name of the Token
TOKEN_NAME = 'ICO Template'

# Symbol of the Token
TOKEN_SYMBOL = 'ICO'

# Number of decimal places
TOKEN_DECIMALS = 8

# Initial Supply of tokens in the system
TOKEN_INITIAL_SUPPLY = 10_000_000 * 100_000_000  # 10m total supply * 10^8 (decimals)


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
    return is_administrator()


def is_administrator() -> bool:
    """
    Validates if the invoker has administrative rights

    :return: whether the contract's invoker is an administrator
    """
    return check_witness(TOKEN_OWNER)


def is_valid_address(address: bytes) -> bool:
    """
    Validates if the address passed through the kyc.

    :return: whether the given address is validated by kyc
    """
    return get(KYC_WHITELIST_PREFIX + address).to_int() > 0


@public
def deploy() -> bool:
    """
    Initializes the storage when the smart contract is deployed.

    :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
    """
    if not check_witness(TOKEN_OWNER):
        return False

    if get(TOKEN_TOTAL_SUPPLY_PREFIX).to_int() > 0:
        return False

    put(TOKEN_TOTAL_SUPPLY_PREFIX, TOKEN_INITIAL_SUPPLY)
    put(TOKEN_OWNER, TOKEN_INITIAL_SUPPLY)

    on_transfer(b'', TOKEN_OWNER, TOKEN_INITIAL_SUPPLY)
    return True


@public
def mint(amount: int) -> bool:
    """
    Mints new tokens

    :param amount: the amount of gas to be refunded
    :type amount: int
    :return: whether the refund was successful
    """
    assert amount > 0
    if not is_administrator():
        return False

    current_total_supply = totalSupply()
    owner_balance = balanceOf(TOKEN_OWNER)

    put(TOKEN_TOTAL_SUPPLY_PREFIX, current_total_supply + amount)
    put(TOKEN_OWNER, owner_balance + amount)

    on_transfer(b'', TOKEN_OWNER, amount)
    return True


@public
def refund(address: bytes, neo_amount: int, gas_amount: int) -> bool:
    """
    Refunds an address with given Neo and Gas

    :param address: the address that have the tokens
    :type address: bytes
    :param neo_amount: the amount of neo to be refunded
    :type neo_amount: int
    :param gas_amount: the amount of gas to be refunded
    :type gas_amount: int
    :return: whether the refund was successful
    """
    assert len(address) == 20
    assert neo_amount > 0 or gas_amount > 0

    if not is_administrator():
        return False

    if neo_amount > 0:
        result = call_contract(NEO, 'transfer', [calling_script_hash, address, neo_amount])
        if result != True:
            # due to a current limitation in the neo3-boa, changing the condition to `not result`
            # will result in a compiler error
            return False

    if gas_amount > 0:
        result = call_contract(GAS, 'transfer', [calling_script_hash, address, neo_amount])
        if result != True:
            # due to a current limitation in the neo3-boa, changing the condition to `not result`
            # will result in a compiler error
            return False

    return True


# -------------------------------------------
# Public methods from NEP5.1
# -------------------------------------------


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
    return get(TOKEN_TOTAL_SUPPLY_PREFIX).to_int()


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
    return get(account).to_int()


@public
def transfer(from_address: bytes, to_address: bytes, amount: int) -> bool:
    """
    Transfers a specified amount of NEP5 tokens from one account to another

    If the method succeeds, it must fire the `transfer` event and must return true, even if the amount is 0,
    or from and to are the same address.

    :param from_address: the address to transfer from
    :type from_address: bytes
    :param to_address: the address to transfer to
    :type to_address: bytes
    :param amount: the amount of NEP5 tokens to transfer
    :type amount: int

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

    # if the method succeeds, it must fire the transfer event, and must return true
    on_transfer(from_address, to_address, amount)
    return True


@public
def allowance(from_address: bytes, to_address: bytes) -> int:
    """
    Returns the amount of tokens that the to account can transfer from the from account.

    :param from_address: the address that have the tokens
    :type from_address: bytes
    :param to_address: the address that is authorized to use the tokens
    :type to_address: bytes

    :return: the amount of tokens that the `to` account can transfer from the `from` account
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(from_address) == 20 and len(to_address) == 20
    return get(TRANSFER_ALLOWANCE_PREFIX + from_address + to_address).to_int()


@public
def transferFrom(originator: bytes, from_address: bytes, to_address: bytes, amount: int) -> bool:
    """
    Transfers an amount from the `from` account to the `to` account if the `originator` has been approved to transfer
    the requested amount.

    :param originator: the address where the actual token is
    :type originator: bytes
    :param from_address: the address to transfer from with originator's approval
    :type from_address: bytes
    :param to_address: the address to transfer to
    :type to_address: bytes
    :param amount: the amount of NEP5 tokens to transfer
    :type amount: int

    :return: whether the transfer was successful
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` if less than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(originator) == 20 and len(from_address) == 20 and len(to_address) == 20
    # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
    assert amount >= 0

    # The function should check whether the from address equals the caller contract hash.
    # If so, the transfer should be processed;
    # If not, the function should use the check_witness to verify the transfer.
    if from_address != calling_script_hash:
        if not check_witness(from_address):
            return False

    # if the `to_address` is a deployed contract, the function should check the payable flag of this contract
    # TODO: include example when objects are implemented

    approved_transfer_amount = allowance(originator, from_address)
    if approved_transfer_amount < amount:
        return False

    originator_balance = balanceOf(originator)
    if originator_balance < amount:
        return False

    # don't accept a meaningless value
    if amount == 0 or originator == to_address or from_address == to_address:
        return True  # nep5 standard: return true when amount is 0 or from == to

    # update allowance between originator and from
    if approved_transfer_amount == amount:
        delete(TRANSFER_ALLOWANCE_PREFIX + originator + from_address)
    else:
        put(TRANSFER_ALLOWANCE_PREFIX + originator + from_address, approved_transfer_amount - amount)

    # update originator's balance
    if originator_balance == amount:
        delete(originator)
    else:
        put(originator, originator_balance - amount)

    # updates to's balance
    to_balance = get(to_address).to_int()
    put(to_address, to_balance + amount)

    # if the method succeeds, it must fire the transfer event, and must return true
    on_transfer(from_address, to_address, amount)
    return True


@public
def approve(originator: bytes, to_address: bytes, amount: int) -> bool:
    """
    Approves the to account to transfer amount tokens from the originator account.

    :param originator: the address that have the tokens
    :type originator: bytes
    :param to_address: the address that is authorized to use the tokens
    :type to_address: bytes
    :param amount: the amount of NEP5 tokens to transfer
    :type amount: int

    :return: whether the approval was successful
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` if less than zero.
    """
    assert len(originator) == 20 and len(to_address) == 20
    assert amount >= 0

    if not check_witness(originator):
        return False

    if originator == to_address:
        return False

    if not is_valid_address(originator) or not is_valid_address(to_address):
        # one of the address doesn't passed the kyc yet
        return False

    if balanceOf(originator) < amount:
        return False

    put(TRANSFER_ALLOWANCE_PREFIX + originator + to_address, amount)
    return True


# -------------------------------------------
# Public methods from KYC
# -------------------------------------------


@public
def kyc_register(addresses: List[bytes]) -> int:
    """
    Includes the given addresses to the kyc whitelist

    :param addresses: a list with the addresses to be included
    :return: the number of included addresses
    """
    included_addresses = 0
    if is_administrator():
        for address in addresses:
            if len(address) == 20:
                kyc_key = KYC_WHITELIST_PREFIX + address
                put(kyc_key, True)
                included_addresses += 1

    return included_addresses


@public
def kyc_remove(addresses: List[bytes]) -> int:
    """
    Removes the given addresses from the kyc whitelist

    :param addresses: a list with the addresses to be removed
    :return: the number of removed addresses
    """
    removed_addresses = 0
    if is_administrator():
        for address in addresses:
            if len(address) == 20:
                kyc_key = KYC_WHITELIST_PREFIX + address
                delete(kyc_key)
                removed_addresses += 1

    return removed_addresses
