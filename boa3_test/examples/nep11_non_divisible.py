# WARNING: This example is currently not fully functional and is being used mainly to test if the NEP-11 in the
# supported_standards at the metadata correctly verifies the methods, for examples that are fully functional check
# https://github.com/CityOfZion/props and https://github.com/OnBlockIO/NEP11TemplatePy

from typing import Any, Optional, Union, cast

from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.contract import Nep11TransferEvent, abort
from boa3.builtin.interop import runtime, storage
from boa3.builtin.interop.contract import GAS as GAS_SCRIPT, call_contract
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.interop.stdlib import deserialize, serialize
from boa3.builtin.nativecontract.contractmanagement import ContractManagement
from boa3.builtin.type import ByteString, UInt160


# -------------------------------------------
# METADATA
# -------------------------------------------

@metadata
def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.supported_standards = ['NEP-11']
    meta.add_permission(methods=['onNEP11Payment'])

    meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
    meta.description = "A simplified NEP-11 example"
    meta.email = "contact@coz.io"
    return meta


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


SUPPLY_KEY = 'totalSupply'

# Symbol of the Token
TOKEN_SYMBOL = 'NEP11'

# Number of decimal places
TOKEN_DECIMALS = 0

# Value of this NEP-11 token compared to GAS
AMOUNT_PER_GAS = 2 * 10 ** 8

# Prefixes
PREFIX_ACCOUNT = b'a'
PREFIX_TOKEN = b't'

# -------------------------------------------
# Events
# -------------------------------------------


on_transfer = Nep11TransferEvent


# -------------------------------------------
# Methods
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
    Since the token managed in this contract is indivisible, the function SHOULD return 0.
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
    return storage.get(SUPPLY_KEY).to_int()


@public(name='balanceOf', safe=True)
def balance_of(owner_address: UInt160) -> int:
    """
    Get the total amount of NFTs owned by an address.

    The parameter account must be a 20-byte address represented by a UInt160.

    :param owner_address: the account address to retrieve the balance for
    :type owner_address: UInt160
    """
    assert len(owner_address) == 20

    balance = 0

    owner: Account = get_account(owner_address)
    if not isinstance(owner, None):
        balance = owner.balance

    return balance


@public(name='tokensOf', safe=True)
def tokens_of(owner: UInt160) -> Iterator:
    """
    Get a iterator with all token ids owned by an address. The values inside the Iterator SHOULD be a ByteString with a
    length of no more than 64 bytes.

    The parameter owner must be a 20-byte address represented by a UInt160.

    :param owner: the account address to retrieve the balance for
    :type owner: UInt160
    """
    assert len(owner) == 20

    return storage.find(account_prefix_key(owner))


@public(name='ownerOf', safe=True)
def owner_of(token_id: ByteString) -> UInt160:
    """
    Get the owner of the specified token.

    The parameter token_id SHOULD be a valid NFT ID (64 bytes maximum).

    :param token_id: the id of a token
    :type token_id: str
    """
    assert len(token_id) <= 64

    owner = UInt160()

    token_bytes = storage.get(account_prefix_key + token_id)
    if len(token_bytes) != 0:
        token = cast(NFT, deserialize(token_bytes))
        owner = token.owner

    return owner


@public
def transfer(to_address: UInt160, token_id: ByteString, data: Any) -> bool:
    """
    Transfers a NFT from one account to another.

    If the method succeeds, it must fire the `Transfer` event and must return true, even if the receiver and sender are
    the same address.

    :param to_address: the address to transfer to
    :type to_address: UInt160
    :param token_id: the id of the token that will be transferred
    :type token_id: int
    :param data: whatever data is pertinent to the onPayment method
    :type data: Any

    :return: whether the transfer was successful
    :raise AssertionError: raised if `to_address` length is not 20 or if `token_id` length is greater than 64.
    """
    pass


def post_transfer(from_address: Union[UInt160, None], to_address: Union[UInt160, None], token_id: ByteString, data: Any):
    """
    Checks if the one receiving NEP11 tokens is a smart contract and if it's one the onPayment method will be called.

    :param from_address: the address of the sender
    :type from_address: UInt160
    :param to_address: the address of the receiver
    :type to_address: UInt160
    :param token_id: the id of the token that is being sent
    :type token_id: ByteString
    :param data: any pertinent data that might validate the transaction
    :type data: Any
    """
    # the transfer event will be fired
    on_transfer(from_address, to_address, 1, token_id)

    if not isinstance(to_address, None):
        contract = ContractManagement.get_contract(to_address)
        if not isinstance(contract, None):
            call_contract(to_address, 'onNEP11Payment', [from_address, 1, token_id, data])


@public
def _deploy(data: Any, update: bool):
    """
    Initializes the storage when the smart contract is deployed.

    :return: whether the deploy was successful. This method must return True only during the smart contract's deploy.
    """
    if not update:
        storage.put(SUPPLY_KEY, 0)


@public(name='onNEP11Payment')
def on_nep11_payment(from_address: UInt160, amount: int, token_id: ByteString, data: Any):
    """
    This contract will not receive another NEP-11 token.

    :param from_address: the address of the one who is trying to send cryptocurrency to this smart contract
    :type from_address: UInt160
    :param amount: the amount of cryptocurrency that is being sent to the this smart contract
    :type amount: int
    :param token_id: the id of the token that is being sent
    :type token_id: ByteString
    :param data: any pertinent data that might validate the transaction
    :type data: Any
    """
    abort()


@public
def onNEP17Payment(from_address: UInt160, amount: int, data: Any):
    """
    NEP-17 affirms :"if the receiver is a deployed contract, the function MUST call onPayment method on receiver
    contract with the data parameter from transfer AFTER firing the Transfer event. If the receiver doesn't want to
    receive this transfer it MUST call ABORT." Therefore, since this is a smart contract, onPayment must exists.

    There is no guideline as to how it should verify the transaction and it's up to the user to make this verification.

    For instance, this onPayment method checks if this smart contract is receiving GAS so that it can mint a NEP11
    token, else it will abort.

    :param from_address: the address of the one who is trying to send cryptocurrency to this smart contract
    :type from_address: UInt160
    :param amount: the amount of cryptocurrency that is being sent to the this smart contract
    :type amount: int
    :param data: any pertinent data that might validate the transaction
    :type data: Any
    """
    if runtime.calling_script_hash == GAS_SCRIPT:
        corresponding_amount = amount // AMOUNT_PER_GAS
        mint(from_address, corresponding_amount)
    else:
        abort()


def mint(account_address: UInt160, amount: int):
    """
    Mints new tokens. This is not a NEP-11 standard method, it's only being use to complement to generate a new NFT
    whenever a user decides to buy one.

    :param account_address: the address of the account that is sending cryptocurrency to this contract
    :type account_address: UInt160
    :param amount: the amount of gas to be refunded
    :type amount: int
    :raise AssertionError: raised if amount is less than than 0
    """
    assert amount >= 0
    account = get_account(account_address)
    if isinstance(account, None):
        account = Account(account_address)

    for x in range(amount):
        NFT(account_address)

        nft_id = storage.get(SUPPLY_KEY)

        account.register_token(nft_id)

        post_transfer(None, account_address, nft_id, None)


# -------------------------------------------
# NFT class
# -------------------------------------------


class NFT:
    def __init__(self, owner: UInt160):
        self.owner: UInt160 = owner

        # since this is an example, the attributes will be generated using the number of NFTs in the contract, but in
        # a real contract it should be some sort of RNG instead
        number = total_supply()
        self.attr1 = (number + 10) * 10 % 9 + 1
        self.attr2 = (number + 10) * 10 % 6 + 1

        current_supply = total_supply() + 1
        storage.put(SUPPLY_KEY, current_supply)
        set_nft(current_supply.to_bytes(), self)

    def change_owner(self, new_owner: UInt160):
        self.owner = new_owner

# -------------------------------------------
# Account class
# -------------------------------------------


class Account:
    def __init__(self, address: UInt160):
        self.address: UInt160 = address
        self._balance: int = 0

    @property
    def balance(self) -> int:
        return self._balance

    def register_token(self, token_id: bytes):
        storage.put(account_prefix_key(self.address) + token_id, True)
        self._balance = self._balance + 1
        self.set_account()

    def remove_token(self, token_id: bytes):
        storage.delete(account_prefix_key(self.address) + token_id)
        self._balance = self._balance - 1
        self.set_account()

    def set_account(self):
        storage.put(PREFIX_ACCOUNT + self.address, serialize(self))

# -------------------------------------------
# Storage helpers
# -------------------------------------------


def account_prefix_key(account: UInt160) -> bytes:
    return PREFIX_ACCOUNT + account + b'_'


def get_account(account: UInt160) -> Optional[Account]:
    account_bytes = storage.get(PREFIX_ACCOUNT + account)
    if len(account_bytes) == 0:
        return None
    return cast(Account, deserialize(account_bytes))


def set_nft(token_id: bytes, token: NFT):
    storage.put(PREFIX_TOKEN + token_id, serialize(token))
