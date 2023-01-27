from typing import Any

from boa3_test.test_drive.neoxp.command.neoexpresscommand import NeoExpressCommand


def create_checkpoint(checkpoint_path: str, force: bool = False) -> NeoExpressCommand:
    options = {}
    if force:
        options['--force'] = ''

    return NeoExpressCommand('checkpoint create', [checkpoint_path], options)


def reset() -> NeoExpressCommand:
    options = {'--force': ''}
    return NeoExpressCommand('reset', options=options)


def fastfwd(block_count: int) -> NeoExpressCommand:
    if not isinstance(block_count, int) or block_count < 1:
        block_count = 1

    options = {}
    return NeoExpressCommand('fastfwd', [str(block_count)], options)


def transfer(sender: str, receiver: str, quantity: int, asset: str, data: Any = None) -> NeoExpressCommand:
    options = {}
    if data is not None:
        import json
        options['--data'] = json.dumps(data)

    return NeoExpressCommand('transfer', [str(quantity), asset, sender, receiver], options)
