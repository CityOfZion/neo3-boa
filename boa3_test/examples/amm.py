from typing import Any, List, Union

from boa3.builtin.compile_time import CreateNewEvent, NeoMetadata, public
from boa3.builtin.contract import Nep17TransferEvent, abort
from boa3.builtin.interop import runtime, storage
from boa3.builtin.interop.blockchain import Transaction
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.math import sqrt
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
    meta.supported_standards = ['NEP-17']
    meta.add_permission(methods=['onNEP17Payment', 'allowance', 'transfer', 'transferFrom'])

    meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
    meta.description = "Automated Market Maker Example"
    meta.email = "contact@coz.io"
    return meta


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


SUPPLY_KEY = b'totalSupply'

# Symbol of the Token
TOKEN_SYMBOL = 'AMM'

# Number of decimal places
TOKEN_DECIMALS = 8

# Percentage of tokens owned by a certain address
PERCENTAGE_PREFIX = b'percentage_prefix'

# Address of token_a and token_b
TOKEN_A = b'token_a_address'
TOKEN_B = b'token_b_address'

# Whether the smart contract was deployed or not
DEPLOYED = b'deployed'

# The fee for doing a swap. 1000 is 100%, 3 is 0.3% and so on
FEE = 3


# -------------------------------------------
# Events
# -------------------------------------------


on_transfer = Nep17TransferEvent

on_sync = CreateNewEvent(
    [
        ('reserve_token_a', int),
        ('reserve_token_b', int)
    ],
    'Sync'
)

on_mint = CreateNewEvent(
    [
        ('sender', UInt160),
        ('amount_token_a', int),
        ('amount_token_b', int)
    ],
    'Mint'
)

on_burn = CreateNewEvent(
    [
        ('sender', UInt160),
        ('amount_token_a', int),
        ('amount_token_b', int)
    ],
    'Burn'
)

on_swap = CreateNewEvent(
    [
        ('sender', UInt160),
        ('amount_token_a_in', int),
        ('amount_token_b_in', int),
        ('amount_token_a_out', int),
        ('amount_token_b_out', int)
    ],
    'Swap'
)


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

    :return: the total token supply deployed in the system.
    """
    return type_helper.to_int(storage.get(SUPPLY_KEY))


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
    Transfers an amount of AMM tokens from one account to another

    If the method succeeds, it must fire the `Transfer` event and must return true, even if the amount is 0,
    or from and to are the same address.

    :param from_address: the address to transfer from
    :type from_address: UInt160
    :param to_address: the address to transfer to
    :type to_address: UInt160
    :param amount: the amount of AMM tokens to transfer
    :type amount: int
    :param data: whatever data is pertinent to the onPayment method
    :type data: Any

    :return: whether the transfer was successful
    :raise AssertionError: raised if `from_address` or `to_address` length is not 20 or if `amount` is less than zero.
    """
    # the parameters from and to should be 20-byte addresses. If not, this method should throw an exception.
    assert len(from_address) == 20 and len(to_address) == 20
    # the parameter amount must be greater than or equal to 0. If not, this method should throw an exception.
    assert amount >= 0

    # The function MUST return false if the from account balance does not have enough tokens to spend.
    from_balance = type_helper.to_int(storage.get(from_address))
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
            storage.put(from_address, from_balance - amount)

        to_balance = type_helper.to_int(storage.get(to_address))
        storage.put(to_address, to_balance + amount)

    # if the method succeeds, it must fire the transfer event
    on_transfer(from_address, to_address, amount)
    # if the to_address is a smart contract, it must call the contracts onPayment
    post_transfer(from_address, to_address, amount, data)
    # and then it must return true
    return True


def post_transfer(from_address: Union[UInt160, None], to_address: Union[UInt160, None], amount: int, data: Any):
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


@public
def _deploy(data: Any, update: bool):
    """
    Deploy the smart contract in the blockchain.

    :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
    """
    if not update:
        container: Transaction = runtime.script_container
        storage.put(b'owner', container.sender)
        storage.put(DEPLOYED, True)


@public
def onNEP17Payment(from_address: UInt160, amount: int, data: Any):
    if not runtime.calling_script_hash == storage.get(TOKEN_A) and not runtime.calling_script_hash == storage.get(TOKEN_B):
        abort()


# -------------------------------------------
# AMM Methods
# -------------------------------------------


def get_owner() -> UInt160:
    return UInt160(storage.get(b'owner'))


@public
def set_address(address_token_a: UInt160, address_token_b: UInt160) -> bool:
    """
    Stores the addresses of the pair of tokens that will be used in this AMM.

    :param address_token_a: the address of token_a
    :type address_token_a: UInt160
    :param address_token_b: the address of token_b
    :type address_token_b: UInt160
    :return: whether the addresses were updated
    :rtype: bool
    """
    if not runtime.check_witness(get_owner()):
        return False

    if not type_helper.to_bool(storage.get(DEPLOYED)):
        return False

    if storage.get(TOKEN_A) != b'' or storage.get(TOKEN_B) != b'':
        return False

    storage.put(TOKEN_A, address_token_a)
    storage.put(TOKEN_B, address_token_b)

    return True


@public
def get_token_a() -> UInt160:
    return UInt160(storage.get(TOKEN_A))


@public
def get_token_b() -> UInt160:
    return UInt160(storage.get(TOKEN_B))


@public
def get_reserves() -> List[int]:
    """
    Returns how many token_a and token_b tokens are in the pool.

    :return: a list of 2 ints, the value in the first index is reserve of token_a and the second value is the reserve of token_b
    """
    return [type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_A)),
            type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_B))]


@public
def add_liquidity(amount_token_a_desired: int, amount_token_b_desired: int, amount_token_a_min: int, amount_token_b_min: int, user_address: UInt160) -> List[int]:
    """
    Adds liquidity to the pool, minting AMM tokens in the process.

    :param amount_token_a_desired: the quantity of token_a that the user wants to send to the liquidity pool
    :type amount_token_a_desired: int
    :param amount_token_b_desired: the quantity of token_b that the user wants to send to the liquidity pool
    :type amount_token_b_desired: int
    :param amount_token_a_min: the minimum quantity of token_a that the user wants to send to the liquidity pool
    :type amount_token_a_min: int
    :param amount_token_b_min: the minimum quantity of token_b that the user wants to send to the liquidity pool
    :type amount_token_b_min: int
    :param user_address: the user's address
    :type user_address: UInt160

    :return: at index 0 and 1, the amount of token_a and token_b tokens that were transferred, respectively, and at
    index 2 the liquidity created in the mint
    :rtype: list

    :raise AssertionError: raised if the best value of a token is less than the minimum amount desired, if the user
    didn't allow enough money, or if the one calling this function is not the user_address
    """
    assert runtime.check_witness(user_address)

    reserve_token_a = type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_A))
    reserve_token_b = type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_B))
    # If there is no liquidity pool, then the values that will be used to mint and create a pool are the desired ones
    if reserve_token_a == 0 and reserve_token_b == 0:
        amount_token_a = amount_token_a_desired
        amount_token_b = amount_token_b_desired
    # If there is already a liquidity pool, the best value of token_b or token_a will be calculated and then they will be
    # minted and added to the pool
    else:
        amount_token_b_best = quote(amount_token_a_desired, reserve_token_a, reserve_token_b)
        if amount_token_b_best <= amount_token_b_desired:
            assert amount_token_b_best >= amount_token_b_min
            amount_token_a = amount_token_a_desired
            amount_token_b = amount_token_b_best
        else:
            amount_token_a_best = quote(amount_token_b_desired, reserve_token_b, reserve_token_a)
            assert amount_token_a_best <= amount_token_a_desired
            assert amount_token_a_best >= amount_token_a_min
            amount_token_a = amount_token_a_best
            amount_token_b = amount_token_b_desired

    token_a = get_token_a()
    token_b = get_token_b()
    amount_allowed_token_a = call_contract(token_a, 'allowance', [user_address, runtime.executing_script_hash])
    amount_allowed_token_b = call_contract(token_b, 'allowance', [user_address, runtime.executing_script_hash])
    if isinstance(amount_allowed_token_a, int) and isinstance(amount_allowed_token_b, int):
        assert amount_allowed_token_a >= amount_token_a and amount_allowed_token_b >= amount_token_b
    else:
        abort()
    call_contract(token_a, 'transferFrom', [runtime.executing_script_hash, user_address, runtime.executing_script_hash, amount_token_a, None])
    call_contract(token_b, 'transferFrom', [runtime.executing_script_hash, user_address, runtime.executing_script_hash, amount_token_b, None])

    # mint() will return the AMM tokens that were minted
    liquidity = mint(user_address)

    return [amount_token_a, amount_token_b, liquidity]


def mint(user_address: UInt160) -> int:
    """
    Mints AMM tokens, this function will be called by `add_liquidity()`.

    It's best practice to separate `add_liquidity` and `mint` into different contracts, `add_liquidity` should be in a
    Router, while `mint` should be in another smart contract, however, since this is just an example, they both are in
    this same smart contract.

    :param user_address: the address of the user that wants to add liquidity to the pool
    :type user_address: UInt160

    :return: the amount of liquidity tokens that were minted
    :rtype: int

    :raise AssertionError: raised if the liquidity ends up being equal or less than 0
    """
    # reserve_token_a and reserve_token_b are the amount of token_a and token_b tokens that the smart contract has saved in the
    # storage, it's not the actual amount that is in the balance, because the amount is not updated after transferring
    # the token_a and token_b tokens, it will be update only after minting
    reserve_token_a = type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_A))
    reserve_token_b = type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_B))

    # balance_token_a and balance_token_b are the actual amount that are in the balance of this smart contract
    balance_token_a = call_contract(get_token_a(), 'balanceOf', [runtime.executing_script_hash])
    balance_token_b = call_contract(get_token_b(), 'balanceOf', [runtime.executing_script_hash])

    liquidity: int

    if isinstance(balance_token_a, int) and isinstance(balance_token_b, int):
        # amount_token_a and amount_token_b are the quantity of tokens that were deposited in the balance of this smart contract
        amount_token_a = balance_token_a - reserve_token_a
        amount_token_b = balance_token_b - reserve_token_b

        total_supply = type_helper.to_int(storage.get(SUPPLY_KEY))
        # if there are no AMM tokens, then the quantity of AMM tokens that will be minted are calculated multiplying
        # amount_token_a and amount_token_b
        if total_supply == 0:
            liquidity = sqrt(amount_token_b * amount_token_a)
        # if the pool is not empty then the amount of AMM tokens that will be minted are calculated the way shown below
        else:
            liquidity = min(amount_token_a * total_supply // reserve_token_a, amount_token_b * total_supply // reserve_token_b)

        assert liquidity > 0

        # updates the total supply of AMM tokens
        storage.put(SUPPLY_KEY, total_supply + liquidity)
        # change the amount of liquidity the user has
        storage.put(user_address, type_helper.to_int(storage.get(user_address)) + liquidity)
        on_transfer(None, user_address, liquidity)

        update(balance_token_a, balance_token_b)
        on_mint(user_address, amount_token_a, amount_token_b)

    else:
        abort()

    return liquidity


@public
def quote(amount_token1: int, reserve_token1: int, reserve_token2: int) -> int:
    """
    Calculates the amount of token2 tokens that have the same value as the amount_token1.

    :param amount_token1: the amount of token1
    :type amount_token1: int
    :param reserve_token1: how many token1 tokens are in the AMM
    :type reserve_token1: int
    :param reserve_token2: how many token2 tokens are int he AMM
    :type reserve_token2: int

    :return: the amount of token2 tokens equivalent to amount_token1
    :rtype: int

    :raise AssertionError: raised if amount_token1, reserve_token1 or reserve_token2 are equal or less than 0
    """
    assert amount_token1 > 0
    assert reserve_token1 > 0 and reserve_token2 > 0
    return amount_token1 * reserve_token2 // reserve_token1


@public
def remove_liquidity(liquidity: int, amount_token_a_min: int, amount_token_b_min: int, user_address: UInt160) -> List[int]:
    """
    Remove liquidity from the pool, burning the AMM token in the process and giving token_a and token_b back to the user.

    :param liquidity: how much liquidity will be removed from the liquidity pool
    :type liquidity: int
    :param amount_token_a_min: minimum amount of token_a that will be transferred to the user
    :type amount_token_a_min: int
    :param amount_token_b_min: minimum amount of token_b that will be transferred to the user
    :type amount_token_b_min: int
    :param user_address: the user's address
    :type user_address: UInt160

    :return: at index 0 and 1, the amount of token_a and token_b tokens that were transferred, respectively
    :rtype: list

    :raise AssertionError: raised if the user doesn't have enough liquidity, or if the amount of token_a or token_b received after
    burning the liquidity is not greater than the minimum amount that the user wanted, or if the one calling this
    function is not the user_address
    """
    assert runtime.check_witness(user_address)
    assert liquidity <= balance_of(user_address)
    amount = burn(liquidity, user_address)
    # Verify if the amount of token_a and token_b are equal or greater than the minimum amount
    assert amount[0] >= amount_token_a_min and amount[1] >= amount_token_b_min
    return amount


def burn(liquidity: int, user_address: UInt160) -> List[int]:
    """
    Burns AMM tokens, this function will be called by `remove_liquidity()`.

    It's best practice to separate `remove_liquidity` and `mint` into different contracts, `add_liquidity` should be in
    a Router, while `burn` should be in another smart contract, however, since this is just an example, they both are in
    this same smart contract.

    :param liquidity: how many AMM tokens will be removed from the pool
    :type liquidity: int
    :param user_address: the address of the user that wants to remove liquidity of the pool
    :type user_address: int

    :return: at index 0 and 1, the amount of token_a and token_b tokens that were transferred, respectively
    :rtype: list

    :raise AssertionError: raised if amount_token_a or amount_token_b is equal or less than zero
    """
    token_a = get_token_a()
    token_b = get_token_b()
    # balance_token_a and balance_token_b are the actual amount that are in the balance of this smart contract
    balance_token_a = call_contract(token_a, 'balanceOf', [runtime.executing_script_hash])
    balance_token_b = call_contract(token_b, 'balanceOf', [runtime.executing_script_hash])

    amount_token_a: int = 0
    amount_token_b: int = 0

    if isinstance(balance_token_a, int) and isinstance(balance_token_b, int):
        total_supply = type_helper.to_int(storage.get(SUPPLY_KEY))

        # amount_token_a and amount_token_b are the amount that will be transferred to the user after burning the liquidity
        amount_token_a = liquidity * balance_token_a // total_supply
        amount_token_b = liquidity * balance_token_b // total_supply
        assert amount_token_a > 0 and amount_token_b > 0

        # changing the user balance after burning the liquidity
        storage.put(user_address, balance_of(user_address) - liquidity)
        # update the amount of AMM tokens in this smart contract
        storage.put(SUPPLY_KEY, total_supply - liquidity)
        on_transfer(user_address, None, liquidity)

        call_contract(token_a, 'transfer', [runtime.executing_script_hash, user_address, amount_token_a, None])
        call_contract(token_b, 'transfer', [runtime.executing_script_hash, user_address, amount_token_b, None])

        balance_token_a = call_contract(token_a, 'balanceOf', [runtime.executing_script_hash])
        balance_token_b = call_contract(token_b, 'balanceOf', [runtime.executing_script_hash])

        if isinstance(balance_token_a, int) and isinstance(balance_token_b, int):
            update(balance_token_a, balance_token_b)
            on_burn(user_address, amount_token_a, amount_token_b)
        else:
            abort()
    else:
        abort()

    return [amount_token_a, amount_token_b]


def update(balance_token_a: int, balance_token_b: int):
    """
    Updates the value of tokens in the AMM.

    :param balance_token_a: the amount of token_a tokens in the balance of this smart contract
    :type balance_token_a: int
    :param balance_token_b: the amount of token_b tokens in the balance of this smart contract
    :type balance_token_b: int
    """
    storage.put(SUPPLY_KEY + TOKEN_A, balance_token_a)
    storage.put(SUPPLY_KEY + TOKEN_B, balance_token_b)

    on_sync(balance_token_a, balance_token_b)


def swap(amount_token_a_out: int, amount_token_b_out: int, user_address: UInt160):
    """
    Swaps one token with another, this function will be called by `swap_tokens`.

    It's best practice to separate `swap_tokens` and `swap` into different contracts, `swap_tokens` should be in a
    Router, while `swap` should be in another smart contract, however, since this is just an example, they both are in
    this same smart contract.

    :param amount_token_a_out: the amount of token_a that will be given to the user
    :type amount_token_a_out: int
    :param amount_token_b_out: the amount of token_b that will be given to the user
    :type amount_token_b_out: int
    :param user_address: the user's address
    :type user_address: UInt160

    :raise AssertionError: raised if the amount_token_a_out and amount_token_b_out are equal or less than zero, if the
    amount the user is going to receive is greater than the amount in the reserve, if the smart contract didn't receive
    any token from the user, or if the constant k after the swap ends up being lower than the one at the beginning
    """
    assert amount_token_a_out > 0 or amount_token_b_out > 0
    reserve_token_a = type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_A))
    reserve_token_b = type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_B))
    assert amount_token_a_out < reserve_token_a and amount_token_b_out < reserve_token_b

    token_a = get_token_a()
    token_b = get_token_b()
    if amount_token_a_out > 0:
        call_contract(token_a, 'transfer', [runtime.executing_script_hash, user_address, amount_token_a_out, None])
    if amount_token_b_out > 0:
        call_contract(token_b, 'transfer', [runtime.executing_script_hash, user_address, amount_token_b_out, None])

    # balance_token_a and balance_token_b are the actual amount that are in the balance of this smart contract
    balance_token_a = call_contract(token_a, 'balanceOf', [runtime.executing_script_hash])
    balance_token_b = call_contract(token_b, 'balanceOf', [runtime.executing_script_hash])

    if isinstance(balance_token_a, int) and isinstance(balance_token_b, int):
        amount_token_a_in = balance_token_a - (reserve_token_a - amount_token_a_out) if balance_token_a > reserve_token_a - amount_token_a_out else 0
        amount_token_b_in = balance_token_b - (reserve_token_b - amount_token_b_out) if balance_token_b > reserve_token_b - amount_token_b_out else 0

        assert amount_token_a_in > 0 or amount_token_b_in > 0

        balance_token_a_adjusted = balance_token_a * 1000 - amount_token_a_in * FEE
        balance_token_b_adjusted = balance_token_b * 1000 - amount_token_b_in * FEE
        constant_k_new = balance_token_a_adjusted * balance_token_b_adjusted
        constant_k_old = reserve_token_a * 1000 * reserve_token_b * 1000
        assert constant_k_new >= constant_k_old

        update(balance_token_a, balance_token_b)
        on_swap(user_address, amount_token_a_in, amount_token_b_in, amount_token_a_out, amount_token_b_out)

    else:
        abort()


@public
def swap_tokens(amount_in: int, amount_out_min: int, token_in: UInt160, user_address: UInt160) -> int:
    """
    Swaps two tokens with a small fee in the process.

    :param amount_in: the amount of tokens that the user is trying to swap
    :type amount_in: int
    :param amount_out_min: the minimum amount of tokens that the user wants to receive
    :type amount_out_min: int
    :param token_in: the address of the token that the user is trying to use in the swap
    :type token_in: UInt160
    :param user_address: the user's address
    :type user_address: UInt160

    :return: the amount of tokens that the user received from the swap
    :rtype: int
    """
    assert runtime.check_witness(user_address)
    token_a = get_token_a()
    token_b = get_token_b()
    assert token_in == token_a or token_in == token_b

    # Verifies if the user is trying to swap token_a or token_b and set the variables accordingly
    if token_in == token_a:
        reserve_token_in = type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_A))
        reserve_token_out = type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_B))
        amount_token_a_in = amount_in
        amount_token_b_in = 0
    else:
        reserve_token_in = type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_B))
        reserve_token_out = type_helper.to_int(storage.get(SUPPLY_KEY + TOKEN_A))
        amount_token_a_in = 0
        amount_token_b_in = amount_in

    # Calculates the amount of tokens the user will receive
    amount_in_fee = amount_in * (1000 - FEE)
    amount_out = amount_in_fee * reserve_token_out // (reserve_token_in * 1000 + amount_in_fee)
    assert amount_out >= amount_out_min

    # Checks if the user allowed enough tokens
    amount_allowed = call_contract(token_in, 'allowance', [user_address, runtime.executing_script_hash])
    if isinstance(amount_allowed, int):
        assert amount_allowed >= amount_in
    else:
        abort()
    call_contract(token_in, 'transferFrom', [runtime.executing_script_hash, user_address, runtime.executing_script_hash, amount_in, None])

    if amount_token_a_in != 0:
        swap(0, amount_out, user_address)
    else:
        swap(amount_out, 0, user_address)

    return amount_out
