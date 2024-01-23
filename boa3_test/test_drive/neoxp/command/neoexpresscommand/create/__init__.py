from boa3_test.test_drive.neoxp.command.neoexpresscommand.neoexpresscommand import NeoExpressCommand

__all__ = ['CreateCommand']


class CreateCommand(NeoExpressCommand):
    def __init__(self, config_output: str | None = None,
                 node_count: int = None,
                 address_version: int = None,
                 force: bool = False):

        if node_count not in [1, 4, 7]:  # allowed values for node count
            node_count = None

        self.config_output = config_output
        self.node_count = node_count
        self.address_version = address_version
        self.force = force

        command_id = 'create'
        args = []
        if isinstance(config_output, str):
            args.append(config_output)

        super().__init__(command_id, args)

    def _get_options(self) -> dict[str, str]:
        options = super()._get_options()

        if isinstance(self.address_version, int):
            options['--count'] = str(self.address_version)
        if isinstance(self.address_version, int):
            options['--address-version'] = str(self.address_version)
        if self.force:
            options['--force'] = ''

        return options
