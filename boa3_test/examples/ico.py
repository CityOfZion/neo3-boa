from typing import Any

from boa3.sc import runtime, storage
from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.contracts import ContractManagement, GasToken as GAS_TOKEN, NeoToken as NEO_TOKEN
from boa3.sc.types import UInt160
from boa3.sc.utils import Nep17TransferEvent, abort, call_contract


# -------------------------------------------
# METADATA
# -------------------------------------------

def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-17']
    meta.add_permission(methods=['onNEP17Payment'])

    meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
    meta.description = "ICO Example"
    meta.email = "contact@coz.io"
    return meta


# -------------------------------------------
# Storage Key Prefixes
# -------------------------------------------


KYC_WHITELIST_PREFIX = b'KYCWhitelistApproved'
TOKEN_TOTAL_SUPPLY_PREFIX = b'TokenTotalSupply'
TRANSFER_ALLOWANCE_PREFIX = b'TransferAllowancePrefix_'
TOKEN_OWNER_KEY = b'owner'


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


# Symbol of the Token
TOKEN_SYMBOL = 'ICO'

# Number of decimal places
TOKEN_DECIMALS = 8

# Initial Supply of tokens in the system
TOKEN_INITIAL_SUPPLY = 10_000_000 * 10 ** TOKEN_DECIMALS  # 10m total supply * 10^8 (decimals)

# -------------------------------------------
# Events
# -------------------------------------------


on_transfer = Nep17TransferEvent


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
    return runtime.check_witness(get_owner())


def is_valid_address(address: UInt160) -> bool:
    """
    Validates if the address passed through the kyc.

    :return: whether the given address is validated by kyc
    """
    return storage.get_int(KYC_WHITELIST_PREFIX + address) > 0


@public
def _deploy(data: Any, update: bool):
    """
    Initializes the storage when the smart contract is deployed.

    :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
    """
    if not update:
        container = runtime.script_container
        owner = container.sender
        storage.put_uint160(TOKEN_OWNER_KEY, owner)

        storage.put_int(TOKEN_TOTAL_SUPPLY_PREFIX, TOKEN_INITIAL_SUPPLY)
        storage.put_int(owner, TOKEN_INITIAL_SUPPLY)

        on_transfer(None, owner, TOKEN_INITIAL_SUPPLY)


def get_owner() -> UInt160:
    return storage.get_uint160(TOKEN_OWNER_KEY)


@public
def mint(amount: int) -> bool:
    """
    Mints new tokens

    :param amount: the amount tokens to be minted
    :type amount: int
    :return: whether the mint was successful
    """
    assert amount >= 0, 'invalid amount'
    if not is_administrator():
        return False

    token_owner = get_owner()
    if amount > 0:
        current_total_supply = total_supply()
        owner_balance = balance_of(token_owner)

        storage.put_int(TOKEN_TOTAL_SUPPLY_PREFIX, current_total_supply + amount)
        storage.put_int(token_owner, owner_balance + amount)

    on_transfer(None, token_owner, amount)
    post_transfer(None, token_owner, amount, None)
    return True


@public
def refund(address: UInt160, neo_amount: int, gas_amount: int) -> bool:
    """
    Refunds an address with given Neo and Gas

    :param address: the address that have the tokens
    :type address: UInt160
    :param neo_amount: the amount of neo to be refunded
    :type neo_amount: int
    :param gas_amount: the amount of gas to be refunded
    :type gas_amount: int
    :return: whether the refund was successful
    """
    assert len(address) == 20, 'invalid account length'
    assert neo_amount > 0 or gas_amount > 0, 'invalid amount'

    if not is_administrator():
        return False

    if not is_valid_address(address):
        return False

    if neo_amount > 0:
        result = NEO_TOKEN.transfer(runtime.executing_script_hash, address, neo_amount)
        assert result, 'NEO transfer failed'

    if gas_amount > 0:
        result = GAS_TOKEN.transfer(runtime.executing_script_hash, address, gas_amount)
        assert result, 'GAS transfer failed'

    return True


# -------------------------------------------
# Public methods from NEP-17
# -------------------------------------------


@public(safe=True)
def symbol() -> str:
    """
    Gets the symbols of the token.

    This symbol should be short (3-8 characters is recommended), with no whitespace characters or new-lines and should
    be limited to the uppercase latin alphabet (i.e. the 26 letters used in English).
    This method must always return the same value every time it is invoked.

    :return: a short string symbol of the token managed in this contract.
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

    This number mustn't be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
    must return 10,000,000 * 10 ^ decimals.

    :return: the total token supply deployed in the system.
    """
    return storage.get_int(TOKEN_TOTAL_SUPPLY_PREFIX)


@public(name='balanceOf', safe=True)
def balance_of(account: UInt160) -> int:
    """
    Get the current balance of an address

    The parameter account should be a 20-byte address.

    :param account: the account address to retrieve the balance for
    :type account: UInt160

    :return: the token balance of the `account`
    :raise AssertionError: raised if `account` length is not 20.
    """
    assert len(account) == 20, 'invalid account length'
    return storage.get_int(account)


@public
def transfer(from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    """
    Transfers a specified amount of NEP17 tokens from one account to another

    If the method succeeds, it must fire the `transfer` event and must return true, even if the amount is 0,
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
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` if less than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(from_address) == 20 and len(to_address) == 20
    # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
    assert amount >= 0

    # The function MUST return false if the from account balance does not have enough tokens to spend.
    from_balance = storage.get_int(from_address)
    if from_balance < amount:
        return False

    # The function should check whether the from address equals the caller contract hash.
    # If so, the transfer should be processed;
    # If not, the function should use the check_witness to verify the transfer.
    if from_address != runtime.calling_script_hash:
        if not runtime.check_witness(from_address):
            return False

    # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
    if from_address != to_address and amount != 0:
        if from_balance == amount:
            storage.delete(from_address)
        else:
            storage.put_int(from_address, from_balance - amount)

        to_balance = storage.get_int(to_address)
        storage.put_int(to_address, to_balance + amount)

    # if the method succeeds, it must fire the transfer event
    on_transfer(from_address, to_address, amount)
    # if the to_address is a smart contract, it must call the contracts onPayment
    post_transfer(from_address, to_address, amount, data)
    # and then it must return true
    return True


def post_transfer(from_address: UInt160 | None, to_address: UInt160 | None, amount: int, data: Any):
    """
    Checks if the one receiving NEP17 tokens is a smart contract and if it's one the onPayment method will be called

    :param from_address: the address of the sender
    :type from_address: UInt160
    :param to_address: the address of the receiver
    :type to_address: UInt160
    :param amount: the amount of cryptocurrency that is being sent
    :type amount: int
    :param data: any pertinent data that might validate the transaction
    :type data: Any
    """
    if to_address is not None:
        contract = ContractManagement.get_contract(to_address)
        if contract is not None:
            call_contract(to_address, 'onNEP17Payment', [from_address, amount, data])


@public(name='onNEP17Payment')
def on_nep17_payment(from_address: UInt160 | None, amount: int, data: Any):
    """
    NEP-17 affirms :"if the receiver is a deployed contract, the function MUST call onPayment method on receiver
    contract with the data parameter from transfer AFTER firing the Transfer event. If the receiver doesn't want to
    receive this transfer it MUST call ABORT." Therefore, since this is a smart contract, onPayment must exist.

    There is no guideline as to how it should verify the transaction and it's up to the user to make this verification.

    For instance, this onPayment method checks if this smart contract is receiving NEO or GAS so that it can mint a
    NEP17 token. If it's not receiving a native token, than it will abort.

    :param from_address: the address of the one who is trying to send cryptocurrency to this smart contract
    :type from_address: UInt160
    :param amount: the amount of cryptocurrency that is being sent to this smart contract
    :type amount: int
    :param data: any pertinent data that might validate the transaction
    :type data: Any
    """
    if from_address is None:
        return

    # Use calling_script_hash to identify if the incoming token is NEO or GAS
    caller = runtime.calling_script_hash
    if caller != NEO_TOKEN.hash and caller != GAS_TOKEN.hash:
        abort()


@public
def allowance(from_address: UInt160, to_address: UInt160) -> int:
    """
    Returns the amount of tokens that the to account can transfer from the from account.

    :param from_address: the address that have the tokens
    :type from_address: UInt160
    :param to_address: the address that is authorized to use the tokens
    :type to_address: UInt160

    :return: the amount of tokens that the `to` account can transfer from the `from` account
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(from_address) == 20 and len(to_address) == 20
    return storage.get_int(TRANSFER_ALLOWANCE_PREFIX + from_address + to_address)


@public(name='transferFrom')
def transfer_from(originator: UInt160, from_address: UInt160, to_address: UInt160, amount: int, data: Any) -> bool:
    """
    Transfers an amount from the `from` account to the `to` account if the `originator` has been approved to transfer
    the requested amount.

    :param originator: the address where the actual token is
    :type originator: UInt160
    :param from_address: the address to transfer from with originator's approval
    :type from_address: UInt160
    :param to_address: the address to transfer to
    :type to_address: UInt160
    :param amount: the amount of NEP17 tokens to transfer
    :type amount: int
    :param data: any pertinent data that might validate the transaction
    :type data: Any

    :return: whether the transfer was successful
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` if less than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(originator) == 20 and len(from_address) == 20 and len(to_address) == 20, 'invalid account length'
    # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
    assert amount >= 0, 'invalid amount'

    # The function should check whether the from address equals the caller contract hash.
    # If so, the transfer should be processed;
    # If not, the function should use the check_witness to verify the transfer.
    if from_address != runtime.calling_script_hash:
        if not runtime.check_witness(from_address):
            return False

    approved_transfer_amount = allowance(originator, from_address)
    if approved_transfer_amount < amount:
        return False

    originator_balance = balance_of(originator)
    if originator_balance < amount:
        return False

    # update allowance between originator and from
    if approved_transfer_amount == amount:
        storage.delete(TRANSFER_ALLOWANCE_PREFIX + originator + from_address)
    else:
        storage.put_int(TRANSFER_ALLOWANCE_PREFIX + originator + from_address, approved_transfer_amount - amount)

    # skip balance changes if transferring to yourself or transferring 0 cryptocurrency
    if amount != 0 and from_address != to_address:
        # update originator's balance
        if originator_balance == amount:
            storage.delete(originator)
        else:
            storage.put_int(originator, originator_balance - amount)

        # updates to's balance
        to_balance = storage.get_int(to_address)
        storage.put_int(to_address, to_balance + amount)

    # if the method succeeds, it must fire the transfer event
    on_transfer(from_address, to_address, amount)
    # if the to_address is a smart contract, it must call the contracts onPayment
    post_transfer(from_address, to_address, amount, data)
    # and then it must return true
    return True


@public
def approve(originator: UInt160, to_address: UInt160, amount: int) -> bool:
    """
    Approves the to account to transfer amount tokens from the originator account.

    :param originator: the address that have the tokens
    :type originator: UInt160
    :param to_address: the address that is authorized to use the tokens
    :type to_address: UInt160
    :param amount: the amount of NEP17 tokens to transfer
    :type amount: int

    :return: whether the approval was successful
    :raise AssertionError: raised if `originator` or `to_address` length is not 20 or if `amount` if less than zero.
    """
    assert len(originator) == 20 and len(to_address) == 20, 'invalid account length'
    assert amount >= 0, 'invalid amount'

    if not runtime.check_witness(originator):
        return False

    if originator == to_address:
        return False

    if not is_valid_address(originator) or not is_valid_address(to_address):
        # one of the addresses didn't pass the kyc
        return False

    if balance_of(originator) < amount:
        return False

    storage.put_int(TRANSFER_ALLOWANCE_PREFIX + originator + to_address, amount)
    return True


# -------------------------------------------
# Public methods from KYC
# -------------------------------------------


@public
def kyc_register(addresses: list[UInt160]) -> int:
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
                storage.put_bool(kyc_key, True)
                included_addresses += 1

    return included_addresses


@public
def kyc_remove(addresses: list[UInt160]) -> int:
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
                storage.delete(kyc_key)
                removed_addresses += 1

    return removed_addresses
