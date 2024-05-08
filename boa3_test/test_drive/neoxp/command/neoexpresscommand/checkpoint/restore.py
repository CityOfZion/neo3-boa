from boa3_test.test_drive.neoxp.command.neoexpresscommand.checkpoint.icheckpointcommand import ICheckpointCommand


class CheckpointRestoreCommand(ICheckpointCommand):
    def __init__(self, file_name: str | None = None,
                 force: bool = False,
                 neo_express_data_file: str = None):

        self.file_name = file_name
        self.force = force
        self.input = neo_express_data_file

        args = []
        if isinstance(file_name, str):
            args.append(file_name)

        super().__init__('restore', args)

    def _get_options(self) -> dict[str, str]:
        options = super()._get_options()

        if self.force:
            options['--force'] = ''

        return options
