from typing import Any

from boa3.builtin.compile_time import CreateNewEvent, NeoMetadata, public
from boa3.builtin.interop import storage, runtime
from boa3.builtin.interop.runtime import check_witness
from boa3.builtin.nativecontract.contractmanagement import ContractManagement
from boa3.builtin.type import UInt160

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
    meta.description = "Update Contract Example. This contract represents the first smart contract deployed on the" \
                       "blockchain, with a buggy method."
    meta.email = "contact@coz.io"

    # requires access to ContractManagement methods
    meta.add_permission(contract='0xfffdc93764dbaddd97c48f252a53ea4643faa3fd',
                        methods=['update'])
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
    This method is not working as intended and ends up giving tokens to a user whenever he wants.
    """
    # some omitted code
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


def get_owner() -> UInt160:
    """
    Gets the script hash of the owner (the account that deployed this smart contract)
    """
    return storage.get_uint160(OWNER_KEY)
