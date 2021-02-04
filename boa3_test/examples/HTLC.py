from typing import Any

from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.contract import abort
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.interop.crypto import hash160
from boa3.builtin.interop.runtime import calling_script_hash, check_witness, executing_script_hash, get_time
from boa3.builtin.interop.storage import get, put
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
    return meta


# -------------------------------------------
# VARIABLES SETTINGS
# -------------------------------------------

OWNER = UInt160()
OTHER_PERSON: bytes = b'person b'
ADDRESS_PREFIX: bytes = b'address'
AMOUNT_PREFIX: bytes = b'amount'
TOKEN_PREFIX: bytes = b'token'
FUNDED_PREFIX: bytes = b'funded'

# Number of seconds that need to pass before refunding the contract
LOCK_TIME = 15 * 1

NOT_INITIALIZED: bytes = b'not initialized'
START_TIME: bytes = b'start time'
SECRET_HASH: bytes = b'secret hash'
DEPLOYED: bytes = b'deployed'


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
    return check_witness(OWNER)


@public
def deploy() -> bool:
    """
    Initializes OWNER and change values of NOT_INITIALIZED and DEPLOYED when the smart contract is deployed.

    :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
    """
    if not check_witness(OWNER):
        return False
    if get(DEPLOYED).to_bool():
        return False

    put(OWNER, OWNER)
    put(NOT_INITIALIZED, True)
    put(DEPLOYED, True)
    return True


@public
def atomic_swap(owner_address: UInt160, owner_token: bytes, owner_amount: int, other_person_address: UInt160,
                other_person_token: bytes, other_person_amount: int, secret_hash: bytes) -> bool:
    """
    Initializes the storage when the atomic swap starts.

    :param owner_address: address of owner
    :type owner_address: UInt160
    :param owner_token: other_person's desired token
    :type owner_token: bytes
    :param owner_amount: other_person's desired amount of tokens
    :type owner_amount: int
    :param other_person_address: address of other_person
    :type other_person_address: bytes
    :param other_person_token: owner's desired token
    :type other_person_token: bytes
    :param other_person_amount: owner's desired amount of tokens
    :type other_person_amount: int
    :param secret_hash: the secret hash created by the contract deployer
    :type secret_hash: bytes

    :return: whether the deploy was successful or not
    :rtype: bool

    :raise AssertionError: raised if `owner_address` or `other_person_address` length is not 20 or if `amount` is not
    greater than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(owner_address) == 20 and len(other_person_address) == 20
    # the parameter amount must be greater than 0. If not, this method should throw an exception.
    assert owner_amount > 0 and other_person_amount > 0

    if get(NOT_INITIALIZED).to_bool() and verify():
        put(ADDRESS_PREFIX + OWNER, owner_address)
        put(TOKEN_PREFIX + OWNER, owner_token)
        put(AMOUNT_PREFIX + OWNER, owner_amount)
        put(ADDRESS_PREFIX + OTHER_PERSON, other_person_address)
        put(TOKEN_PREFIX + OTHER_PERSON, other_person_token)
        put(AMOUNT_PREFIX + OTHER_PERSON, other_person_amount)
        put(SECRET_HASH, secret_hash)
        put(NOT_INITIALIZED, False)
        put(START_TIME, get_time)
        return True
    return False


@public
def onNEP17Payment(from_address: UInt160, amount: int, data: Any):
    """
    Since this is a deployed contract, transfer will be calling this onPayment method with the data parameter from
    transfer. If someone is doing a not required transfer, then ABORT will be called.

    :param from_address: the address of the one who is trying to transfer cryptocurrency to this smart contract
    :type from_address: UInt160
    :param amount: the amount of cryptocurrency that is being sent to this smart contract
    :type amount: int
    :param data: any pertinent data that may validate the transaction
    :type data: Any

    :raise AssertionError: raised if `from_address` length is not 20
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(from_address) == 20

    if not get(NOT_INITIALIZED).to_bool():
        # Used to check if the one who's transferring to this contract is the OWNER
        address = get(ADDRESS_PREFIX + OWNER)
        # Used to check if OWNER already transfer to this smart contract
        funded_crypto = get(FUNDED_PREFIX + OWNER).to_int()
        # Used to check if OWNER is transferring the correct amount
        amount_crypto = get(AMOUNT_PREFIX + OWNER).to_int()
        # Used to check if OWNER is transferring the correct token
        token_crypto = get(TOKEN_PREFIX + OWNER)
        if (from_address == address and
                funded_crypto == 0 and
                amount == amount_crypto and
                calling_script_hash == token_crypto):
            put(FUNDED_PREFIX + OWNER, amount)
            return
        else:
            # Used to check if the one who's transferring to this contract is the OTHER_PERSON
            address = get(ADDRESS_PREFIX + OTHER_PERSON)
            # Used to check if OTHER_PERSON already transfer to this smart contract
            funded_crypto = get(FUNDED_PREFIX + OTHER_PERSON).to_int()
            # Used to check if OTHER_PERSON is transferring the correct amount
            amount_crypto = get(AMOUNT_PREFIX + OTHER_PERSON).to_int()
            # Used to check if OTHER_PERSON is transferring the correct token
            token_crypto = get(TOKEN_PREFIX + OTHER_PERSON)
            if (from_address == address and
                    funded_crypto == 0 and
                    amount == amount_crypto and
                    calling_script_hash == token_crypto):
                put(FUNDED_PREFIX + OTHER_PERSON, amount)
                return
    abort()


@public
def withdraw(secret: str) -> bool:
    """
    Deposits the contract's cryptocurrency into the owner and other_person addresses as long as they both transferred
    to this contract and there is some time remaining

    :param secret: the private key that unlocks the transaction
    :type secret: str

    :return: whether the transfers were successful
    :rtype: bool
    """
    # Checking if OWNER and OTHER_PERSON transferred to this smart contract
    funded_owner = get(FUNDED_PREFIX + OWNER).to_int()
    funded_other_person = get(FUNDED_PREFIX + OTHER_PERSON).to_int()
    if verify() and not refund() and hash160(secret) == get(SECRET_HASH) and funded_owner != 0 and funded_other_person != 0:
        put(FUNDED_PREFIX + OWNER, 0)
        put(FUNDED_PREFIX + OTHER_PERSON, 0)
        put(NOT_INITIALIZED, True)
        put(START_TIME, 0)
        call_contract(UInt160(get(TOKEN_PREFIX + OTHER_PERSON)), 'transfer',
                      [executing_script_hash, get(ADDRESS_PREFIX + OWNER), get(AMOUNT_PREFIX + OTHER_PERSON), ''])
        call_contract(UInt160(get(TOKEN_PREFIX + OWNER)), 'transfer',
                      [executing_script_hash, get(ADDRESS_PREFIX + OTHER_PERSON), get(AMOUNT_PREFIX + OWNER), ''])
        return True

    return False


@public
def refund() -> bool:
    """
    If the atomic swap didn't occur in time, refunds the cryptocurrency that was deposited in this smart contract

    :return: whether enough time has passed and the cryptocurrencies were refunded
    :rtype: bool
    """
    if get_time > get(START_TIME).to_int() + LOCK_TIME:

        # Checking if OWNER transferred to this smart contract
        funded_crypto = get(FUNDED_PREFIX + OWNER).to_int()
        if funded_crypto != 0:
            call_contract(UInt160(get(TOKEN_PREFIX + OWNER)), 'transfer',
                          [executing_script_hash, get(ADDRESS_PREFIX + OWNER), get(AMOUNT_PREFIX + OWNER)])

        # Checking if OTHER_PERSON transferred to this smart contract
        funded_crypto = get(FUNDED_PREFIX + OTHER_PERSON).to_int()
        if funded_crypto != 0:
            call_contract(UInt160(get(TOKEN_PREFIX + OTHER_PERSON)), 'transfer',
                          [executing_script_hash, get(ADDRESS_PREFIX + OTHER_PERSON), get(AMOUNT_PREFIX + OTHER_PERSON)])

        put(FUNDED_PREFIX + OWNER, 0)
        put(FUNDED_PREFIX + OTHER_PERSON, 0)
        put(NOT_INITIALIZED, True)
        put(START_TIME, 0)
        return True
    return False
