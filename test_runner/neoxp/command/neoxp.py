from test_runner.neoxp.command.neoexpresscommand import NeoExpressCommand


def create_checkpoint(checkpoint_path: str, force: bool = False) -> NeoExpressCommand:
    options = {}
    if force:
        options['--force'] = ''

    return NeoExpressCommand('checkpoint create', [checkpoint_path], options)


def fastfwd(block_count: int) -> NeoExpressCommand:
    if not isinstance(block_count, int) or block_count < 1:
        block_count = 1

    options = {}
    return NeoExpressCommand('fastfwd', [str(block_count)], options)
