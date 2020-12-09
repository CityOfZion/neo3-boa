from typing import Any

from boa3.builtin import NeoMetadata, metadata, public
from boa3.builtin.interop.contract import NEO, GAS
from boa3.builtin.interop.runtime import calling_script_hash, log
from boa3.builtin.contract import abort
from boa3.builtin.interop.runtime import check_witness, executing_script_hash
from boa3.builtin.interop.storage import get, put


@metadata
def manifest_metadata() -> NeoMetadata:
    """
    Defines this smart contract's metadata information
    """
    meta = NeoMetadata()
    return meta


# Script hash of the contract owner
OWNER = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
NEO_BALANCE_KEY= "NEO"
GAS_BALANCE_KEY= "GAS"

@public
def onPayment(from_address: bytes, amount: int, data: Any):
    #Use the asset hash to identify what kind of token is coming
    assetHash = calling_script_hash
    if assetHash == NEO:
        #Received NEO
        log("Received NEO")
        currentNeoBalance = get(NEO_BALANCE_KEY)
        #This is an example. This is not needed
        put(NEO_BALANCE_KEY, currentNeoBalance + amount)
    elif assetHash == GAS:
        #Receive GAS
        log ("Received GAS")
        currentGasBalance = get(GAS_BALANCE_KEY)
        # This is an example. This is not needed
        put(GAS_BALANCE_KEY, currentGasBalance + amount)
    else:
        abort()


@public
def verify() -> bool:
    """
    When this contract address is included in the transaction signature,
    this method will be triggered as a VerificationTrigger to verify that the signature is correct.
    For example, this method needs to be called when withdrawing token from the contract.

    :return: whether the transaction signature is correct
    """
    return check_witness(OWNER)