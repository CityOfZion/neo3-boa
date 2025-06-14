# ------------------------------------------------------------------------------------------------------------------------
# DISCLAIMER: this smart contract was made by GhostMarket and can be found on https://github.com/OnBlockIO/NEP11TemplatePy
# with further instructions on how to modify and use it.
# ------------------------------------------------------------------------------------------------------------------------

from typing import Any, cast

from boa3.sc import storage
from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.contracts import ContractManagement, StdLib
from boa3.sc.runtime import check_witness, get_network, script_container
from boa3.sc.types import FindOptions, UInt160, CallFlags
from boa3.sc.utils import CreateNewEvent, abort, call_contract, get_call_flags
from boa3.sc.utils import to_bytes
from boa3.sc.utils.iterator import Iterator


# -------------------------------------------
# METADATA
# -------------------------------------------

def gm_manifest() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.author = "Template Author"  # TODO_TEMPLATE
    meta.description = "Some Description"  # TODO_TEMPLATE
    meta.email = "hello@example.com"  # TODO_TEMPLATE
    meta.supported_standards = ["NEP-11"]
    meta.source = "https://github.com/"  # TODO_TEMPLATE
    meta.add_permission(contract='*', methods=['onNEP11Payment'])
    return meta


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------

# Symbol of the Token
TOKEN_SYMBOL = 'EXMP'  # TODO_TEMPLATE

# Number of decimal places
TOKEN_DECIMALS = 0

# Whether the smart contract was deployed or not
DEPLOYED = b'deployed'

# Whether the smart contract is paused or not
PAUSED = b'paused'

# -------------------------------------------
# Prefixes
# -------------------------------------------

ACCOUNT_PREFIX = b'ACC'
TOKEN_PREFIX = b'TPF'
TOKEN_DATA_PREFIX = b'TDP'
LOCKED_PREFIX = b'LCP'
BALANCE_PREFIX = b'BLP'
SUPPLY_PREFIX = b'SPP'
META_PREFIX = b'MDP'
LOCKED_VIEW_COUNT_PREFIX = b'LVCP'
ROYALTIES_PREFIX = b'RYP'

# -------------------------------------------
# Keys
# -------------------------------------------

TOKEN_COUNT = b'TOKEN_COUNT'
AUTH_ADDRESSES = b'AUTH_ADDRESSES'

# -------------------------------------------
# Events
# -------------------------------------------

on_transfer = CreateNewEvent(
    # trigger when tokens are transferred, including zero value transfers.
    [
        ('from_addr', UInt160 | None),
        ('to_addr', UInt160 | None),
        ('amount', int),
        ('tokenId', bytes)
    ],
    'Transfer'
)

on_auth = CreateNewEvent(
    # trigger when an address has been authorized/whitelisted.
    [
        ('authorized', UInt160),
        ('type', int),
        ('add', bool),
    ],
    'Authorized'
)

on_unlock = CreateNewEvent(
    [
        ('tokenId', bytes),
        ('counter', int)
    ],
    'UnlockIncremented'
)

# DEBUG_START
# -------------------------------------------
# DEBUG
# -------------------------------------------

on_debug = CreateNewEvent(
    [
        ('params', list),
    ],
    'Debug'
)


def debug(params: list):
    allow_notify = get_call_flags() & CallFlags.ALLOW_NOTIFY
    if allow_notify == CallFlags.ALLOW_NOTIFY:
        on_debug(params)


# DEBUG_END

# -------------------------------------------
# NEP-11 Methods
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
    debug(['symbol: ', TOKEN_SYMBOL])
    return TOKEN_SYMBOL


@public(safe=True)
def decimals() -> int:
    """
    Gets the amount of decimals used by the token.

    E.g. 8, means to divide the token amount by 100,000,000 (10 ^ 8) to get its user representation.
    This method must always return the same value every time it is invoked.

    :return: the number of decimals used by the token.
    """
    debug(['decimals: ', TOKEN_DECIMALS])
    return TOKEN_DECIMALS


@public(safe=True)
def totalSupply() -> int:
    """
    Gets the total token supply deployed in the system.

    This number must not be in its user representation. E.g. if the total supply is 10,000,000 tokens, this method
    must return 10,000,000 * 10 ^ decimals.

    :return: the total token supply deployed in the system.
    """
    debug(['totalSupply: ', storage.get_int(SUPPLY_PREFIX)])
    return storage.get_int(SUPPLY_PREFIX, storage.get_read_only_context())


@public(safe=True)
def balanceOf(owner: UInt160) -> int:
    """
    Get the current balance of an address

    The parameter owner must be a 20-byte address represented by a UInt160.

    :param owner: the owner address to retrieve the balance for
    :type owner: UInt160
    :return: the total amount of tokens owned by the specified address.
    :raise AssertionError: raised if `owner` length is not 20.
    """
    expect(validateAddress(owner), "Not a valid address")
    debug(['balanceOf: ', storage.get_int(mk_balance_key(owner), storage.get_read_only_context())])
    return storage.get_int(mk_balance_key(owner), storage.get_read_only_context())


@public(safe=True)
def tokensOf(owner: UInt160) -> Iterator:
    """
    Get all of the token ids owned by the specified address

    The parameter owner must be a 20-byte address represented by a UInt160.

    :param owner: the owner address to retrieve the tokens for
    :type owner: UInt160
    :return: an iterator that contains all of the token ids owned by the specified address.
    :raise AssertionError: raised if `owner` length is not 20.
    """
    expect(validateAddress(owner), "Not a valid address")
    flags = FindOptions.REMOVE_PREFIX | FindOptions.KEYS_ONLY
    context = storage.get_read_only_context()
    return storage.find(mk_account_key(owner), context, flags)


@public
def transfer(to: UInt160, tokenId: bytes, data: Any) -> bool:
    """
    Transfers the token with id tokenId to address to

    The parameter to SHOULD be a 20-byte address. If not, this method SHOULD throw an exception.
    The parameter tokenId SHOULD be a valid NFT. If not, this method SHOULD throw an exception.
    If the method succeeds, it MUST fire the Transfer event, and MUST return true, even if the token is sent to the owner.
    If the receiver is a deployed contract, the function MUST call onNEP11Payment method on receiver contract with the
    data parameter from transfer AFTER firing the Transfer event.

    The function SHOULD check whether the owner address equals the caller contract hash. If so, the transfer SHOULD be
    processed; If not, the function SHOULD use the SYSCALL Neo.Runtime.CheckWitness to verify the transfer.

    If the transfer is not processed, the function SHOULD return false.

    :param to: the address to transfer to
    :type to: UInt160
    :param tokenId: the token to transfer
    :type tokenId: bytes
    :param data: whatever data is pertinent to the onPayment method
    :type data: Any
    :return: whether the transfer was successful
    :raise AssertionError: raised if `to` length is not 20 or if `tokenId` is not a valid NFT or if the contract is paused.
    """
    expect(validateAddress(to), "Not a valid address")
    expect(not isPaused(), "Contract is currently paused")
    token_owner = get_owner_of(tokenId)
    expect(token_owner != UInt160.zero, "Token not found")

    if not check_witness(token_owner):
        return False

    if token_owner != to:
        set_balance(token_owner, -1)
        remove_token_account(token_owner, tokenId)

        set_balance(to, 1)

        set_owner_of(tokenId, to)
        add_token_account(to, tokenId)
    post_transfer(token_owner, to, tokenId, data)
    return True


def post_transfer(token_owner: UInt160 | None, to: UInt160 | None, tokenId: bytes, data: Any):
    """
    Checks if the one receiving NEP11 tokens is a smart contract and if it's one the onPayment method will be called - internal

    :param token_owner: the address of the sender
    :type token_owner: UInt160
    :param to: the address of the receiver
    :type to: UInt160
    :param tokenId: the token hash as bytes
    :type tokenId: bytes
    :param data: any pertinent data that might validate the transaction
    :type data: Any
    """
    on_transfer(token_owner, to, 1, tokenId)
    if to is not None:
        contract = ContractManagement.get_contract(to)
        if contract is not None:
            call_contract(to, 'onNEP11Payment', [token_owner, 1, tokenId, data])
            pass


@public(safe=True)
def ownerOf(tokenId: bytes) -> UInt160:
    """
    Get the owner of the specified token.

    The parameter tokenId SHOULD be a valid NFT. If not, this method SHOULD throw an exception.

    :param tokenId: the token for which to check the ownership
    :type tokenId: bytes
    :return: the owner of the specified token.
    :raise AssertionError: raised if `tokenId` is not a valid NFT.
    """
    owner = get_owner_of(tokenId)
    debug(['ownerOf: ', owner])
    return owner


@public(safe=True)
def tokens() -> Iterator:
    """
    Get all tokens minted by the contract

    :return: an iterator that contains all of the tokens minted by the contract.
    """
    flags = FindOptions.REMOVE_PREFIX | FindOptions.KEYS_ONLY
    context = storage.get_read_only_context()
    return storage.find(TOKEN_PREFIX, context, flags)


@public(safe=True)
def properties(tokenId: bytes) -> dict[Any, Any]:
    """
    Get the properties of a token.

    The parameter tokenId SHOULD be a valid NFT. If no metadata is found (invalid tokenId), an exception is thrown.

    :param tokenId: the token for which to check the properties
    :type tokenId: bytes
    :return: a serialized NVM object containing the properties for the given NFT.
    :raise AssertionError: raised if `tokenId` is not a valid NFT, or if no metadata available.
    """
    metaBytes = cast(str, get_meta(tokenId))
    expect(len(metaBytes) != 0, 'No metadata available for token')
    metaObject = cast(dict[str, str], StdLib.json_deserialize(metaBytes))

    return metaObject


@public(safe=True)
def propertiesJson(tokenId: bytes) -> str:
    """
    Get the properties of a token.

    The parameter tokenId SHOULD be a valid NFT. If no metadata is found (invalid tokenId), an exception is thrown.

    :param tokenId: the token for which to check the properties
    :type tokenId: bytes
    :return: a serialized NVM object containing the properties for the given NFT.
    :raise AssertionError: raised if `tokenId` is not a valid NFT, or if no metadata available.
    """
    meta = get_meta(tokenId)
    expect(len(meta) != 0, 'No metadata available for token')
    debug(['properties: ', meta])
    return meta


@public
def _deploy(data: Any, upgrade: bool):
    """
    The contracts initial entry point, on deployment.
    """
    debug(["deploy now"])
    if upgrade:
        return

    if storage.get_bool(DEPLOYED, storage.get_read_only_context()):
        return

    tx = script_container
    debug(["tx.sender: ", tx.sender, get_network()])
    owner: UInt160 = tx.sender
    network = get_network()
    # DEBUG_START
    # custom owner for tests, ugly hack, because TestEnginge sets an unkown tx.sender...
    if data is not None and network == 860833102:
        newOwner = cast(UInt160, data)
        debug(["check", newOwner])
        internal_deploy(newOwner)
        return

    if data is None and network == 860833102:
        return
    # DEBUG_END
    debug(["owner: ", owner])
    internal_deploy(owner)


def internal_deploy(owner: UInt160):
    debug(["internal: ", owner])
    storage.put_bool(DEPLOYED, True)
    storage.put_bool(PAUSED, False)
    storage.put_int(TOKEN_COUNT, 0)

    auth: list[UInt160] = []
    auth.append(owner)
    storage.put_list(AUTH_ADDRESSES, auth)


@public(name='onNEP11Payment')
def on_nep11_payment(from_address: UInt160, amount: int, token_id: bytes, data: Any):
    """
    This contract will not receive another NEP-11 token.

    :param from_address: the address of the one who is trying to send cryptocurrency to this smart contract
    :type from_address: UInt160
    :param amount: the amount of cryptocurrency that is being sent to the this smart contract
    :type amount: int
    :param token_id: the id of the token that is being sent
    :type token_id: bytes
    :param data: any pertinent data that might validate the transaction
    :type data: Any
    """
    abort()


# -------------------------------------------
# Methods
# -------------------------------------------

@public
def burn(tokenId: bytes) -> bool:
    """
    Burn a token.

    :param tokenId: the token to burn
    :type tokenId: bytes
    :return: whether the burn was successful.
    :raise AssertionError: raised if the contract is paused.
    """
    expect(not isPaused(), "Contract is currently paused")
    return internal_burn(tokenId)


@public
def mint(account: UInt160, meta: str, lockedContent: str, royalties: str) -> bytes:
    """
    Mint new token.

    :param account: the address of the account that is minting token
    :type account: UInt160
    :param meta: the metadata to use for this token
    :type meta: str
    :param lockedContent: the lock content to use for this token
    :type lockedContent: str
    :param royalties: the royalties to use for this token
    :type royalties: str
    :return: tokenId of the token minted
    :raise AssertionError: raised if the contract is paused or if check witness fails.
    """
    expect(validateAddress(account),
           "Not a valid address")  # not really necessary because check_witness would catch an invalid address
    expect(not isPaused(), "Contract is currently paused")

    # TODO_TEMPLATE: add own logic if necessary, or uncomment below to restrict minting to contract authorized addresses
    # verified: bool = verify()
    # expect(verified, '`account` is not allowed for mint')
    expect(check_witness(account), "Invalid witness")

    return internal_mint(account, meta, lockedContent, royalties)


@public(safe=True)
def getRoyalties(tokenId: bytes) -> str:
    """
    Get a token royalties values.

    :param tokenId: the token to get royalties values
    :type tokenId: bytes
    :return: str of addresses and values for this token royalties.
    :raise AssertionError: raised if any `tokenId` is not a valid NFT.
    """
    royalties = get_royalties(tokenId)
    debug(['getRoyalties: ', royalties])
    return royalties


@public(safe=True)
def getLockedContentViewCount(tokenId: bytes) -> int:
    """
    Get lock content view count of a token.

    :param tokenId: the token to query
    :type tokenId: bytes
    :return: number of times the lock content of this token was accessed.
    """
    debug(['getLockedContentViewCount: ', get_locked_view_counter(tokenId)])
    return get_locked_view_counter(tokenId)


@public
def getLockedContent(tokenId: bytes) -> str:
    """
    Get lock content of a token.

    :param tokenId: the token to query
    :type tokenId: bytes
    :return: the lock content of this token.
    :raise AssertionError: raised if witness is not owner
    :emits UnlockIncremented
    """
    owner = get_owner_of(tokenId)

    expect(check_witness(owner), "Prohibited access to locked content!")
    set_locked_view_counter(tokenId)

    debug(['getLockedContent: ', get_locked_content(tokenId)])
    content = get_locked_content(tokenId)
    counter = get_locked_view_counter(tokenId)
    on_unlock(tokenId, counter)
    return content


@public(safe=True)
def getAuthorizedAddress() -> list[UInt160]:
    """
    Configure authorized addresses.

    When this contract address is included in the transaction signature,
    this method will be triggered as a VerificationTrigger to verify that the signature is correct.
    For example, this method needs to be called when withdrawing token from the contract.

    :return: whether the transaction signature is correct
    :raise AssertionError: raised if witness is not verified.
    """
    auth = cast(list[UInt160], storage.get_list(AUTH_ADDRESSES, storage.get_read_only_context()))

    return auth


@public
def setAuthorizedAddress(address: UInt160, authorized: bool):
    """
    Configure authorized addresses.

    When this contract address is included in the transaction signature,
    this method will be triggered as a VerificationTrigger to verify that the signature is correct.
    For example, this method needs to be called when withdrawing token from the contract.

    :param address: the address of the account that is being authorized
    :type address: UInt160
    :param authorized: authorization status of this address
    :type authorized: bool
    :return: whether the transaction signature is correct
    :raise AssertionError: raised if witness is not verified.
    """
    verified: bool = verify()
    expect(verified, '`account` is not allowed for setAuthorizedAddress')
    expect(validateAddress(address), "Not a valid address")
    expect(isinstance(authorized, bool), "authorized has to be of type bool")
    auth = cast(list[UInt160], storage.get_list(AUTH_ADDRESSES, storage.get_read_only_context()))

    if authorized:
        found = False
        for i in auth:
            if i == address:
                found = True
                break

        if not found:
            auth.append(address)

        storage.put_list(AUTH_ADDRESSES, auth)
        on_auth(address, 0, True)
    else:
        auth.remove(address)
        storage.put_list(AUTH_ADDRESSES, auth)
        on_auth(address, 0, False)


@public
def updatePause(status: bool) -> bool:
    """
    Set contract pause status.

    :param status: the status of the contract pause
    :type status: bool
    :return: the contract pause status
    :raise AssertionError: raised if witness is not verified.
    """
    verified: bool = verify()
    expect(verified, '`account` is not allowed for updatePause')
    expect(isinstance(status, bool), "status has to be of type bool")
    storage.put_bool(PAUSED, status)
    debug(['updatePause: ', storage.get_bool(PAUSED, storage.get_read_only_context())])
    return storage.get_bool(PAUSED, storage.get_read_only_context())


@public(safe=True)
def isPaused() -> bool:
    """
    Get the contract pause status.

    If the contract is paused, some operations are restricted.

    :return: whether the contract is paused
    """
    debug(['isPaused: ', storage.get_bool(PAUSED)])
    if storage.get_bool(PAUSED, storage.get_read_only_context()):
        return True
    return False


@public
def verify() -> bool:
    """
    Check if the address is allowed.

    When this contract address is included in the transaction signature,
    this method will be triggered as a VerificationTrigger to verify that the signature is correct.
    For example, this method needs to be called when withdrawing token from the contract.

    :return: whether the transaction signature is correct
    """
    auth = cast(list[UInt160], storage.get_list(AUTH_ADDRESSES, storage.get_read_only_context()))
    tx = script_container
    for addr in auth:
        if check_witness(addr):
            debug(["Verification successful", addr, tx.sender])
            return True

    debug(["Verification failed", addr])
    return False


@public
def update(script: bytes, manifest: bytes):
    """
    Upgrade the contract.

    :param script: the contract script
    :type script: bytes
    :param manifest: the contract manifest
    :type manifest: bytes
    :raise AssertionError: raised if witness is not verified
    """
    verified: bool = verify()
    expect(verified, '`account` is not allowed for update')
    ContractManagement.update(script, manifest)
    debug(['update called and done'])


@public
def destroy():
    """
    Destroy the contract.

    :raise AssertionError: raised if witness is not verified
    """
    verified: bool = verify()
    expect(verified, '`account` is not allowed for destroy')
    debug(['destroy called and done'])
    ContractManagement.destroy()


def internal_burn(tokenId: bytes) -> bool:
    """
    Burn a token - internal

    :param tokenId: the token to burn
    :type tokenId: bytes
    :return: whether the burn was successful.
    :raise AssertionError: raised if `tokenId` is not a valid NFT.
    """
    owner = get_owner_of(tokenId)

    if not check_witness(owner):
        return False

    remove_owner_of(tokenId)
    set_balance(owner, -1)
    add_to_supply(-1)
    remove_meta(tokenId)
    remove_locked_content(tokenId)
    remove_royalties(tokenId)
    remove_token_account(owner, tokenId)

    post_transfer(owner, None, tokenId, None)
    return True


def internal_mint(account: UInt160, meta: str, lockedContent: str, royalties: str) -> bytes:
    """
    Mint new token - internal

    :param account: the address of the account that is minting token
    :type account: UInt160
    :param meta: the metadata to use for this token
    :type meta: str
    :param lockedContent: the lock content to use for this token
    :type lockedContent: str
    :param royalties: the royalties to use for this token
    :type royalties: str
    :return: tokenId of the token minted
    :raise AssertionError: raised if meta is empty, or if contract is paused.
    """
    expect(len(meta) != 0, '`meta` can not be empty')

    tokenId = storage.get_int(TOKEN_COUNT, storage.get_read_only_context()) + 1
    storage.put_int(TOKEN_COUNT, tokenId)
    tokenIdBytes = to_bytes(tokenId)

    set_owner_of(tokenIdBytes, account)
    set_balance(account, 1)
    add_to_supply(1)

    add_meta(tokenIdBytes, meta)
    debug(['metadata: ', meta])

    if len(lockedContent) != 0:
        add_locked_content(tokenIdBytes, lockedContent)
        debug(['locked: ', lockedContent])

    if len(royalties) != 0:
        add_royalties(tokenIdBytes, cast(str, royalties))
        debug(['royalties: ', royalties])

    add_token_account(account, tokenIdBytes)
    post_transfer(None, account, tokenIdBytes, None)
    return tokenIdBytes


def remove_token_account(holder: UInt160, tokenId: bytes):
    key = mk_account_key(holder) + tokenId
    debug(['add_token_account: ', key, tokenId])
    storage.delete(key)


def add_token_account(holder: UInt160, tokenId: bytes):
    key = mk_account_key(holder) + tokenId
    debug(['add_token_account: ', key, tokenId])
    storage.put(key, tokenId)


def get_owner_of(tokenId: bytes) -> UInt160:
    key = mk_token_key(tokenId)
    debug(['get_owner_of: ', key, tokenId])
    owner = storage.get_uint160(key, storage.get_read_only_context())
    return owner


def remove_owner_of(tokenId: bytes):
    key = mk_token_key(tokenId)
    debug(['remove_owner_of: ', key, tokenId])
    storage.delete(key)


def set_owner_of(tokenId: bytes, owner: UInt160):
    key = mk_token_key(tokenId)
    debug(['set_owner_of: ', key, tokenId])
    storage.put_uint160(key, owner)


def add_to_supply(amount: int):
    total = totalSupply() + amount
    debug(['add_to_supply: ', amount])
    storage.put_int(SUPPLY_PREFIX, total)


def set_balance(owner: UInt160, amount: int):
    old = balanceOf(owner)
    new = old + amount
    debug(['set_balance: ', amount])

    key = mk_balance_key(owner)
    if (new > 0):
        storage.put_int(key, new)
    else:
        storage.delete(key)


def get_meta(tokenId: bytes) -> str:
    key = mk_meta_key(tokenId)
    debug(['get_meta: ', key, tokenId])
    val = storage.get_str(key, storage.get_read_only_context())
    return val


def remove_meta(tokenId: bytes):
    key = mk_meta_key(tokenId)
    debug(['remove_meta: ', key, tokenId])
    storage.delete(key)


def add_meta(tokenId: bytes, meta: str):
    key = mk_meta_key(tokenId)
    debug(['add_meta: ', key, tokenId])
    storage.put_str(key, meta)


def get_locked_content(tokenId: bytes) -> str:
    key = mk_locked_key(tokenId)
    debug(['get_locked_content: ', key, tokenId])
    val = storage.get_str(key, storage.get_read_only_context())
    return val


def remove_locked_content(tokenId: bytes):
    key = mk_locked_key(tokenId)
    debug(['remove_locked_content: ', key, tokenId])
    storage.delete(key)


def add_locked_content(tokenId: bytes, content: str):
    key = mk_locked_key(tokenId)
    debug(['add_locked_content: ', key, tokenId])
    storage.put_str(key, content)


def get_royalties(tokenId: bytes) -> str:
    key = mk_royalties_key(tokenId)
    debug(['get_royalties: ', key, tokenId])
    val = storage.get_str(key, storage.get_read_only_context())
    return val


def add_royalties(tokenId: bytes, royalties: str):
    key = mk_royalties_key(tokenId)
    debug(['add_royalties: ', key, tokenId])
    storage.put_str(key, royalties)


def remove_royalties(tokenId: bytes):
    key = mk_royalties_key(tokenId)
    debug(['remove_royalties: ', key, tokenId])
    storage.delete(key)


def get_locked_view_counter(tokenId: bytes) -> int:
    key = mk_lv_key(tokenId)
    debug(['get_locked_view_counter: ', key, tokenId])
    return storage.get_int(key, storage.get_read_only_context())


def remove_locked_view_counter(tokenId: bytes):
    key = mk_lv_key(tokenId)
    debug(['remove_locked_view_counter: ', key, tokenId])
    storage.delete(key)


def set_locked_view_counter(tokenId: bytes):
    key = mk_lv_key(tokenId)
    debug(['set_locked_view_counter: ', key, tokenId])
    count = storage.get_int(key, storage.get_read_only_context()) + 1
    storage.put_int(key, count)


# helpers

def expect(condition: bool, message: str):
    allow_notify = get_call_flags() & CallFlags.ALLOW_NOTIFY
    if allow_notify == CallFlags.ALLOW_NOTIFY:
        assert condition, message
    else:
        assert condition, message


def validateAddress(address: UInt160) -> bool:
    if not isinstance(address, UInt160):
        return False
    if address == 0:
        return False
    return True


def mk_account_key(address: UInt160) -> bytes:
    return ACCOUNT_PREFIX + address


def mk_balance_key(address: UInt160) -> bytes:
    return BALANCE_PREFIX + address


def mk_token_key(tokenId: bytes) -> bytes:
    return TOKEN_PREFIX + tokenId


def mk_token_data_key(tokenId: bytes) -> bytes:
    return TOKEN_DATA_PREFIX + tokenId


def mk_meta_key(tokenId: bytes) -> bytes:
    return META_PREFIX + tokenId


def mk_locked_key(tokenId: bytes) -> bytes:
    return LOCKED_PREFIX + tokenId


def mk_royalties_key(tokenId: bytes) -> bytes:
    return ROYALTIES_PREFIX + tokenId


def mk_lv_key(tokenId: bytes) -> bytes:
    return LOCKED_VIEW_COUNT_PREFIX + tokenId
