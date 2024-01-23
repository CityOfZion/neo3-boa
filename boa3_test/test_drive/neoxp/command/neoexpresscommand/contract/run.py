from typing import Any

from boa3.internal.neo3.core.types import UInt160
from boa3_test.test_drive.model.network.payloads.witnessscope import WitnessScope
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command import utils
from boa3_test.test_drive.neoxp.command.neoexpresscommand.contract.icontractcommand import IContractCommand


class ContractRunCommand(IContractCommand):
    def __init__(self, contract: str | UInt160, method: str, *args: Any,
                 account: Account = None,
                 witness_scope: WitnessScope = WitnessScope.CalledByEntry,
                 results_only: bool = False,
                 additional_gas: int = 0,
                 wallet_password: str = None,
                 trace: bool = False,
                 json_output: bool = False,
                 neo_express_data_file: str = None):

        self.contract: UInt160 = contract
        self.method = method
        self.args = args

        self.account = account
        self.witness_scope = witness_scope
        self.password = wallet_password

        self.results = True if not isinstance(account, Account) else results_only
        self.additional_gas = additional_gas if additional_gas > 0 else 0
        self.input = neo_express_data_file
        self.trace = trace
        self.json_output = json_output

        arguments = [str(contract), method]
        arguments.extend(args)

        super().__init__('run', arguments)

    def _get_options(self) -> dict[str, str]:
        options = super()._get_options()

        if isinstance(self.account, Account):
            options['--account'] = self.account.get_identifier()
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
