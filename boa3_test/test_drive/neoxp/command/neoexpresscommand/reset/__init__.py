from boa3_test.test_drive.neoxp.command.neoexpresscommand.neoexpresscommand import NeoExpressCommand

__all__ = ['ResetCommand']


class ResetCommand(NeoExpressCommand):
    def __init__(self, node_index: int | None = None,
                 force: bool = False,
                 reset_all: bool = False,
                 neo_express_data_file: str = None):

        self.node_index = node_index
        self.force = force
        self.reset_all = reset_all
        self.input = neo_express_data_file

        command_id = 'reset'
        args = []
        if isinstance(node_index, int):
            args.append(str(node_index))

        super().__init__(command_id, args)

    def _get_options(self) -> dict[str, str]:
        options = super()._get_options()

        if self.force:
            options['--force'] = ''
        if self.reset_all:
            options['--all'] = ''

        return options
