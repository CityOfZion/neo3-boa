from typing import Dict

from boa3_test.test_drive.neoxp.command.neoexpresscommand.contract.icontractcommand import IContractCommand


class ContractListCommand(IContractCommand):
    def __init__(self, json_output: bool = False,
                 neo_express_data_file: str = None):

        self.input = neo_express_data_file
        self.json_output = json_output

        super().__init__('list')

    def _get_options(self) -> Dict[str, str]:
        options = super()._get_options()

        if self.json_output:
            options['--json'] = ''

        return options
