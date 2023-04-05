from typing import Dict

from boa3_test.test_drive.model.network.payloads.witnessscope import WitnessScope
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command import utils
from boa3_test.test_drive.neoxp.command.neoexpresscommand.contract.icontractcommand import IContractCommand


class ContractInvokeCommand(IContractCommand):
    def __init__(self, invoke_file: str, account: Account,
                 witness_scope: WitnessScope = None,
                 results_only: bool = False,
                 additional_gas: int = 0,
                 wallet_password: str = None,
                 trace: bool = False,
                 json_output: bool = False,
                 neo_express_data_file: str = None):

        self.invoke_file = invoke_file
        self.account = account

        self.witness_scope = witness_scope
        self.password = wallet_password

        self.results = True if not isinstance(account, Account) else results_only
        self.additional_gas = additional_gas if additional_gas > 0 else 0
        self.input = neo_express_data_file
        self.trace = trace
        self.json_output = json_output

        super().__init__('invoke', [invoke_file, account.get_identifier()])

    def _get_options(self) -> Dict[str, str]:
        options = super()._get_options()

        if isinstance(self.witness_scope, WitnessScope):
            options['--witness-scope'] = self.witness_scope.name
        if self.results:
            options['--results'] = ''
        if self.additional_gas > 0:
            options['--gas'] = utils.stringify_asset_quantity(self.additional_gas, utils.GAS_DECIMALS)
        if isinstance(self.password, str):
            options['--password'] = self.password
        if self.trace:
            options['--trace'] = ''
        if self.json_output:
            options['--json'] = ''

        return options
