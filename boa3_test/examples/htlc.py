from typing import Any

from boa3.builtin.compile_time import NeoMetadata, public
from boa3.builtin.contract import abort
from boa3.builtin.interop import runtime, storage
from boa3.builtin.interop.blockchain import Transaction
from boa3.builtin.interop.contract import GAS as GAS_SCRIPT, call_contract
from boa3.builtin.interop.crypto import hash160
from boa3.builtin.type import UInt160, helper as type_helper


# -------------------------------------------
# METADATA
# -------------------------------------------

def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.add_permission(methods=['transfer'])
    return meta


# -------------------------------------------
# VARIABLES SETTINGS
# -------------------------------------------


OWNER_KEY = b'owner'
PERSON_A: bytes = b'person a'
PERSON_B: bytes = b'person b'
ADDRESS_PREFIX: bytes = b'address'
AMOUNT_PREFIX: bytes = b'amount'
TOKEN_PREFIX: bytes = b'token'
FUNDED_PREFIX: bytes = b'funded'

# Number of milliseconds that need to pass before refunding the contract
LOCK_TIME = 24 * 60 * (60 * 10 ** 3)    # 1 day in milliseconds

NOT_INITIALIZED: bytes = b'not initialized'
START_TIME: bytes = b'start time'
SECRET_HASH: bytes = b'secret hash'


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
    return runtime.check_witness(get_owner())


@public
def _deploy(data: Any, update: bool):
    """
    Initializes OWNER_KEY and change values of NOT_INITIALIZED and DEPLOYED when the smart contract is deployed.

    :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
    """
    if not update:
        container: Transaction = runtime.script_container

        storage.put(OWNER_KEY, container.sender)
        storage.put(NOT_INITIALIZED, True)


@public
def atomic_swap(person_a_address: UInt160, person_a_token: UInt160, person_a_amount: int, person_b_address: UInt160,
                person_b_token: UInt160, person_b_amount: int, secret_hash: bytes) -> bool:
    """
    Initializes the storage when the atomic swap starts.

    :param person_a_address: address of person_a
    :type person_a_address: UInt160
    :param person_a_token: person_b's desired token
    :type person_a_token: UInt160
    :param person_a_amount: person_b's desired amount of tokens
    :type person_a_amount: int
    :param person_b_address: address of person_b
    :type person_b_address: bytes
    :param person_b_token: person_a's desired token
    :type person_b_token: UInt160
    :param person_b_amount: person_a's desired amount of tokens
    :type person_b_amount: int
    :param secret_hash: the secret hash created by the contract deployer
    :type secret_hash: bytes

    :return: whether the deploy was successful or not
    :rtype: bool

    :raise AssertionError: raised if `person_a_address` or `person_b_address` length is not 20 or if `amount` is not
    greater than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(person_a_address) == 20 and len(person_b_address) == 20
    # the parameter amount must be greater than 0. If not, this method should throw an exception.
    assert person_a_amount > 0 and person_b_amount > 0

    if type_helper.to_bool(storage.get(NOT_INITIALIZED)) and verify():
        storage.put(ADDRESS_PREFIX + PERSON_A, person_a_address)
        storage.put(TOKEN_PREFIX + PERSON_A, person_a_token)
        storage.put(AMOUNT_PREFIX + PERSON_A, person_a_amount)
        storage.put(ADDRESS_PREFIX + PERSON_B, person_b_address)
        storage.put(TOKEN_PREFIX + PERSON_B, person_b_token)
        storage.put(AMOUNT_PREFIX + PERSON_B, person_b_amount)
        storage.put(SECRET_HASH, secret_hash)
        storage.put(NOT_INITIALIZED, False)
        storage.put(START_TIME, runtime.time)
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
    if from_address is not None:
        assert len(from_address) == 20

    # this validation will verify if Neo is trying to mint GAS to this smart contract
    if from_address is None and runtime.calling_script_hash == GAS_SCRIPT:
        return

    if not type_helper.to_bool(storage.get(NOT_INITIALIZED)):
        # Used to check if the one who's transferring to this contract is the PERSON_A
        address = storage.get(ADDRESS_PREFIX + PERSON_A)
        # Used to check if PERSON_A has already transferred to this smart contract
        funded_crypto = type_helper.to_int(storage.get(FUNDED_PREFIX + PERSON_A))
        # Used to check if PERSON_A is transferring the correct amount
        amount_crypto = type_helper.to_int(storage.get(AMOUNT_PREFIX + PERSON_A))
        # Used to check if PERSON_A is transferring the correct token
        token_crypto = storage.get(TOKEN_PREFIX + PERSON_A)
        if (from_address == address and
                funded_crypto == 0 and
                amount == amount_crypto and
                runtime.calling_script_hash == token_crypto):
            storage.put(FUNDED_PREFIX + PERSON_A, amount)
            return
        else:
            # Used to check if the one who's transferring to this contract is the OTHER_PERSON
            address = storage.get(ADDRESS_PREFIX + PERSON_B)
            # Used to check if PERSON_B already transfer to this smart contract
            funded_crypto = type_helper.to_int(storage.get(FUNDED_PREFIX + PERSON_B))
            # Used to check if PERSON_B is transferring the correct amount
            amount_crypto = type_helper.to_int(storage.get(AMOUNT_PREFIX + PERSON_B))
            # Used to check if PERSON_B is transferring the correct token
            token_crypto = storage.get(TOKEN_PREFIX + PERSON_B)
            if (from_address == address and
                    funded_crypto == 0 and
                    amount == amount_crypto and
                    runtime.calling_script_hash == token_crypto):
                storage.put(FUNDED_PREFIX + PERSON_B, amount)
                return
    abort()


@public
def withdraw(secret: str) -> bool:
    """
    Deposits the contract's cryptocurrency into the person_a and person_b addresses as long as they both transferred
    to this contract and there is some time remaining

    :param secret: the private key that unlocks the transaction
    :type secret: str

    :return: whether the transfers were successful
    :rtype: bool
    """
    # Checking if PERSON_A and PERSON_B transferred to this smart contract
    funded_person_a = type_helper.to_int(storage.get(FUNDED_PREFIX + PERSON_A))
    funded_person_b = type_helper.to_int(storage.get(FUNDED_PREFIX + PERSON_B))
    if verify() and not refund() and hash160(secret) == storage.get(SECRET_HASH) and funded_person_a != 0 and funded_person_b != 0:
        storage.put(FUNDED_PREFIX + PERSON_A, 0)
        storage.put(FUNDED_PREFIX + PERSON_B, 0)
        storage.put(NOT_INITIALIZED, True)
        storage.put(START_TIME, 0)
        call_contract(UInt160(storage.get(TOKEN_PREFIX + PERSON_B)), 'transfer',
                      [runtime.executing_script_hash, storage.get(ADDRESS_PREFIX + PERSON_A),
                       type_helper.to_int(storage.get(AMOUNT_PREFIX + PERSON_B)), None])
        call_contract(UInt160(storage.get(TOKEN_PREFIX + PERSON_A)), 'transfer',
                      [runtime.executing_script_hash, storage.get(ADDRESS_PREFIX + PERSON_B),
                       type_helper.to_int(storage.get(AMOUNT_PREFIX + PERSON_A)), None])
        return True

    return False


@public
def refund() -> bool:
    """
    If the atomic swap didn't occur in time, refunds the cryptocurrency that was deposited in this smart contract

    :return: whether enough time has passed and the cryptocurrencies were refunded
    :rtype: bool
    """
    if runtime.time > type_helper.to_int(storage.get(START_TIME)) + LOCK_TIME:
        # Checking if PERSON_A transferred to this smart contract
        funded_crypto = type_helper.to_int(storage.get(FUNDED_PREFIX + PERSON_A))
        if funded_crypto != 0:
            call_contract(UInt160(storage.get(TOKEN_PREFIX + PERSON_A)), 'transfer',
                          [runtime.executing_script_hash, UInt160(storage.get(ADDRESS_PREFIX + PERSON_A)),
                           type_helper.to_int(storage.get(AMOUNT_PREFIX + PERSON_A)), None])

        # Checking if PERSON_B transferred to this smart contract
        funded_crypto = type_helper.to_int(storage.get(FUNDED_PREFIX + PERSON_B))
        if funded_crypto != 0:
            call_contract(UInt160(storage.get(TOKEN_PREFIX + PERSON_B)), 'transfer',
                          [runtime.executing_script_hash, storage.get(ADDRESS_PREFIX + PERSON_B),
                           type_helper.to_int(storage.get(AMOUNT_PREFIX + PERSON_B)), None])
        storage.put(FUNDED_PREFIX + PERSON_A, 0)
        storage.put(FUNDED_PREFIX + PERSON_B, 0)
        storage.put(NOT_INITIALIZED, True)
        storage.put(START_TIME, 0)
        return True
    return False


def get_owner() -> UInt160:
    """
    Gets the script hash of the owner (the account that deployed this smart contract)
    """
    return UInt160(storage.get(OWNER_KEY))
