from typing import Any

from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.utils import CreateNewEvent
from boa3.sc.runtime import check_witness
from boa3.sc.contracts import ContractManagement
from boa3.sc.types import UInt160
from boa3.sc import storage, runtime

# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


# The keys used to access the storage
OWNER_KEY = b'owner'
SUPPLY_KEY = b'totalSupply'

TOKEN_TOTAL_SUPPLY = 10_000_000 * 10 ** 8  # 10m total supply * 10^8 (decimals)


# -------------------------------------------
# METADATA
# -------------------------------------------

def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information.
    """
    meta = NeoMetadata()

    meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
    meta.description = "Update Contract Example. This contract represents the updated smart contract to be deployed " \
                       "on the blockchain, with the method now working properly"
    meta.email = "contact@coz.io"
    return meta


# -------------------------------------------
# Events
# -------------------------------------------


on_transfer = CreateNewEvent(
    [
        ('from_addr', UInt160 | None),
        ('to_addr', UInt160 | None),
        ('amount', int)
    ],
    'Transfer'
)


# -------------------------------------------
# Methods
# -------------------------------------------

@public
def update_sc(nef_file: bytes, manifest: bytes, data: Any = None):
    """
    Updates the smart contract. In this example there is a bugged method, so, the smart contract will be updated to fix
    the bug.
    """
    if check_witness(get_owner()):
        ContractManagement.update(nef_file, manifest, data)


@public
def method(account: UInt160):
    """
    This method is now working properly.
    """
    # some omitted code

    # now there is a verification to this method
    if check_witness(get_owner()):
        storage.put_int(account, storage.get_int(account) + 2 * 10 ** 8)
        on_transfer(None, account, 2 * 10 ** 8)
    # more omitted code


@public
def _deploy(data: Any, update: bool):
    """
    Initializes the storage when the smart contract is deployed. When this smart contract is updated, it should do nothing.
    """
    if not update:
        container = runtime.script_container

        storage.put_int(SUPPLY_KEY, TOKEN_TOTAL_SUPPLY)
        storage.put_int(container.sender, TOKEN_TOTAL_SUPPLY)
        storage.put_uint160(OWNER_KEY, container.sender)
        on_transfer(None, container.sender, TOKEN_TOTAL_SUPPLY)


@public(name='balanceOf', safe=True)
def balance_of(account: UInt160) -> int:
    """
    Get the current balance of an address.
    """
    assert len(account) == 20
    return storage.get_int(account)


@public
def get_name() -> str:
    return 'Test Contract'


def get_owner() -> UInt160:
    """
    Gets the script hash of the owner (the account that deployed this smart contract)
    """
    return storage.get_uint160(OWNER_KEY)
