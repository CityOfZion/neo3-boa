import json
from typing import Any, Dict

from boa3_test.test_drive.model.network.payloads.witnessscope import WitnessScope
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command.neoexpresscommand.contract.icontractcommand import IContractCommand


class ContractDeployCommand(IContractCommand):
    def __init__(self, contract_nef: str, account: Account,
                 witness_scope: WitnessScope = WitnessScope.CalledByEntry,
                 data: Any = None,
                 wallet_password: str = None,
                 trace: bool = False,
                 force: bool = False,
                 json_output: bool = False,
                 neo_express_data_file: str = None):

        self.contract_nef = contract_nef
        self.account = account

        self.witness_scope = witness_scope
        self.data = data
        self.password = wallet_password

        self.input = neo_express_data_file
        self.trace = trace
        self.force = force
        self.json_output = json_output

        super().__init__('deploy', [contract_nef, account.get_identifier()])

    def _get_options(self) -> Dict[str, str]:
        options = super()._get_options()

        if isinstance(self.witness_scope, WitnessScope):
            options['--witness-scope'] = self.witness_scope.name
        if self.data is not None:
            options['--data'] = json.dumps(self.data)
        if isinstance(self.password, str):
            options['--password'] = self.password
        if self.trace:
            options['--trace'] = ''
        if self.force:
            options['--force'] = ''
        if self.json_output:
            options['--json'] = ''

        return options
