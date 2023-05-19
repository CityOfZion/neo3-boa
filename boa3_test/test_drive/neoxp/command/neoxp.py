from typing import Any, Union

from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command import neoexpresscommand as neoxp
from boa3_test.test_drive.neoxp.command import neoxp_contract as contract
from boa3_test.test_drive.neoxp.command import neoxp_oracle as oracle
from boa3_test.test_drive.neoxp.command.neoexpresscommand import NeoExpressCommand


def create_checkpoint(checkpoint_path: str, force: bool = False) -> NeoExpressCommand:
    return neoxp.checkpoint.CheckpointCreateCommand(checkpoint_path, force=force)


def reset() -> NeoExpressCommand:
    return neoxp.reset.ResetCommand(force=True)


def fastfwd(block_count: int, time_interval_in_secs: int = 0) -> NeoExpressCommand:
    if not isinstance(block_count, int) or block_count < 1:
        block_count = 1

    return neoxp.fastforward.FastForwardCommand(block_count, time_interval_in_secs)


def transfer(sender: Account, receiver: Account, asset: str,
             quantity: Union[int, float], decimals: int = 0,
             data: Any = None) -> NeoExpressCommand:

    return neoxp.transfer.TransferAssetCommand(asset, sender, receiver, quantity,
                                               decimals=decimals,
                                               data=data)
