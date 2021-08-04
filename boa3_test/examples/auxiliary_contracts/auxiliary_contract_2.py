from typing import Any

from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop.contract import call_contract
from boa3.builtin.type import UInt160


# This smart contract is being used to call methods that require the calling_scripthash. Right now it is returning None
# when the TestEngine is the one calling the function.
# Though, in the future, the TestEngine will return the correct address, rendering this smart contract useless
# TODO: delete this smart contract and change wrapped neo tests when the TestEngine gets updated

# -------------------------------------------
# METADATA
# -------------------------------------------


@metadata
def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.author = "Mirella Medeiros, Ricardo Prado and Lucas Uezu. COZ in partnership with Simpli"
    meta.description = "Another smart contract that will help during test"
    meta.email = "contact@coz.io"
    return meta


@public
def calling_transfer(address: UInt160, from_address: UInt160, to_address: UInt160, amount: UInt160, data: Any) -> Any:
    """
    Transfer NEO to an account

    :return: whether the transfer was successful.
    :rtype: bool
    """
    return call_contract(address, 'transfer', [from_address, to_address, amount, data])


# Always accept cryptocurrency
@public
def onNEP17Payment(from_address: UInt160, amount: int, data: Any):
    pass
