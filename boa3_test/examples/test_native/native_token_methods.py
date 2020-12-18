from typing import Any

from boa3.builtin.type import UInt160
from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop.contract import call_contract, NEO, GAS
from boa3.builtin.interop.runtime import calling_script_hash


# -------------------------------------------
# METADATA
# -------------------------------------------

@metadata
def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    meta.author = "COZ"
    meta.description = "NEP-17 Example"
    meta.email = "contact@coz.io"
    return meta


@public
def transfer_neo(to_address: UInt160, amount: UInt160, data: Any) -> bool:
    """
    Transfer NEO to an account

    :return: whether the transfer was successful.
    :rtype: bool
    """
    return call_contract(NEO, 'transfer', [calling_script_hash, to_address, amount, data])


@public
def transfer_gas(to_address: UInt160, amount: UInt160, data: Any) -> bool:
    """
    Transfer GAS to an account

    :return: whether the transfer was successful.
    :rtype: bool
    """
    return call_contract(GAS, 'transfer', [calling_script_hash, to_address, amount, data])


@public
def balanceOf_neo(account: UInt160) -> int:
    """
    Checks the balance of NEO at an account
    """
    return call_contract(NEO, 'balanceOf', [account])


@public
def balanceOf_gas(account: UInt160) -> int:
    """
    Checks the balance of GAS at an account
    """
    return call_contract(GAS, 'balanceOf', [account])
