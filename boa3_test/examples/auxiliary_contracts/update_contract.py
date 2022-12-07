from typing import Any, Union

from boa3.builtin import CreateNewEvent, NeoMetadata, metadata, public
from boa3.builtin.interop import storage
from boa3.builtin.interop.runtime import check_witness
from boa3.builtin.nativecontract.contractmanagement import ContractManagement
from boa3.builtin.type import UInt160

# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------


# Script hash of the contract owner
OWNER = UInt160()
SUPPLY_KEY = 'totalSupply'
TOKEN_TOTAL_SUPPLY = 10_000_000 * 10 ** 8  # 10m total supply * 10^8 (decimals)


# -------------------------------------------
# METADATA
# -------------------------------------------


@metadata
def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information.
    """
    meta = NeoMetadata()

    meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
    meta.description = "Update Contract Example. This contract represents the updated smart contract to be deployed " \
                       "on the blockchain, with the method now working properly"
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
        ('from_addr', Union[UInt160, None]),
        ('to_addr', Union[UInt160, None]),
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
    if check_witness(OWNER):
        ContractManagement.update(nef_file, manifest, data)


@public
def method(account: UInt160):
    """
    This method is now working properly.
    """
    # some omitted code

    # now there is a verification to this method
    if check_witness(OWNER):
        storage.put(account, storage.get(account).to_int() + 2 * 10 ** 8)
        on_transfer(None, account, 2 * 10 ** 8)
    # more omitted code


@public
def _deploy(data: Any, update: bool):
    """
    Initializes the storage when the smart contract is deployed. When this smart contract is updated, it should do nothing.
    """
    if not update:
        storage.put(SUPPLY_KEY, TOKEN_TOTAL_SUPPLY)
        storage.put(OWNER, TOKEN_TOTAL_SUPPLY)
        on_transfer(None, OWNER, TOKEN_TOTAL_SUPPLY)


@public(name='balanceOf', safe=True)
def balance_of(account: UInt160) -> int:
    """
    Get the current balance of an address.
    """
    assert len(account) == 20
    return storage.get(account).to_int()


@public
def get_name() -> str:
    return 'Test Contract'
