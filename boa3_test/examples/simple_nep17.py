from typing import Any, Union

from boa3.builtin.compile_time import NeoMetadata, public
from boa3.builtin.contract import Nep17TransferEvent, abort
from boa3.builtin.interop import runtime, storage
from boa3.builtin.interop.blockchain import Transaction
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.nativecontract.contractmanagement import ContractManagement
from boa3.builtin.type import UInt160, helper as type_helper


# -------------------------------------------
# METADATA
# -------------------------------------------

def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.name = 'NEP-17 Test Coin Contract'
    meta.supported_standards = ['NEP-17']
    meta.add_permission(methods=['onNEP17Payment'])

    meta.author = "COZ in partnership with Simpli"
    meta.description = "A simpler NEP-17 Example"
    meta.email = "contact@coz.io"
    return meta


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


# Symbol of the Token
TOKEN_SYMBOL = 'COIN'

# Number of decimal places
TOKEN_DECIMALS = 2

# Total Supply of tokens in the system
TOKEN_TOTAL_SUPPLY = 100_000_000 * 10 ** TOKEN_DECIMALS     # 100_000_000,00 total supply

# -------------------------------------------
# Events
# -------------------------------------------


on_transfer = Nep17TransferEvent


# -------------------------------------------
# NEP-17 Methods
# -------------------------------------------


@public(safe=True)
def symbol() -> str:
    """
    Gets the symbols of the token.

    This string must be valid ASCII, must not contain whitespace or control characters, should be limited to uppercase
    Latin alphabet (i.e. the 26 letters used in English) and should be short (3-8 characters is recommended).
    This method must always return the same value every time it is invoked.

    :return: a short string representing symbol of the token managed in this contract.
    """
    return TOKEN_SYMBOL


@public(safe=True)
def decimals() -> int:
    """
    Gets the amount of decimals used by the token.

    E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
    This method must always return the same value every time it is invoked.

    :return: the number of decimals used by the token.
    """
    return TOKEN_DECIMALS


@public(name='totalSupply', safe=True)
def total_supply() -> int:
    """
    Gets the total token supply deployed in the system.

    This number must not be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
    must return 10,000,000 * 10 ^ decimals.

    We will only mint the tokens once, so we can just return a constant value instead of having to save it on the
    storage.

    :return: the total token supply deployed in the system.
    """
    return TOKEN_TOTAL_SUPPLY


@public(name='balanceOf', safe=True)
def balance_of(account: UInt160) -> int:
    """
    Get the current balance of an address

    The parameter account must be a 20-byte address represented by a UInt160.

    :param account: the account address to retrieve the balance for
    :type account: UInt160
    """
    assert len(account) == 20
    return type_helper.to_int(storage.get(account))


@public
def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    """
    Transfers an amount of NEP17 tokens from one account to another

    If the method succeeds, it must fire the `Transfer` event and must return true, even if the amount is 0,
    or from and to are the same address.

    :param from_address: the address to transfer from
    :type from_address: UInt160
    :param to_address: the address to transfer to
    :type to_address: UInt160
    :param amount: the amount of NEP17 tokens to transfer
    :type amount: int
    :param data: whatever data is pertinent to the onPayment method
    :type data: Any

    :return: whether the transfer was successful
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` is less than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    from_balance = balance_of(from_address)
    to_balance = balance_of(to_address)
    # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
    assert amount >= 0

    # The function MUST return false if the from account balance does not have enough tokens to spend.
    if from_balance < amount:
        return False

    # The function will use the check_witness to verify the transfer.
    if not runtime.check_witness(from_address):
        return False

    # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
    if from_address != to_address and amount != 0:
        if from_balance == amount:
            storage.delete(from_address)
        else:
            storage.put(from_address, from_balance - amount)

        storage.put(to_address, to_balance + amount)

    # if the method succeeds, it must fire the transfer event
    on_transfer(from_address, to_address, amount)
    # if the to_address is a smart contract, it must call the contracts onPayment
    if ContractManagement.get_contract(to_address) is not None:
        call_contract(to_address, 'onNEP17Payment', [from_address, amount, data])
    # and then it must return true
    return True


@public(name='onNEP17Payment')
def on_nep17_payment(from_address: Union[UInt160, None], amount: int, data: Any):
    """
    NEP-17 affirms: "if the receiver is a deployed contract, the function MUST call onPayment method on receiver
    contract with the data parameter from transfer AFTER firing the Transfer event. If the receiver doesn't want to
    receive this transfer it MUST call ABORT." Therefore, since this is a smart contract, onPayment must exist.

    There is no guideline as to how it should verify the transaction, and it's up to the user to make this verification.

    For instance, this onNEP17Payment will always abort when someone tries to send any fungible token to it.

    :param from_address: the address of the one who is trying to send cryptocurrency to this smart contract
    :type from_address: UInt160
    :param amount: the amount of cryptocurrency that is being sent to this smart contract
    :type amount: int
    :param data: any pertinent data that might validate the transaction
    :type data: Any
    """
    abort()


@public
def _deploy(data: Any, update: bool):
    """
    Initializes the storage when the smart contract is deployed. Sending all tokens to the deployer account
    """
    if not update:
        container: Transaction = runtime.script_container

        storage.put(container.sender, total_supply())

        on_transfer(None, container.sender, total_supply())
