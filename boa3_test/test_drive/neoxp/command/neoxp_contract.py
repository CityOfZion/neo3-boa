from boa3_test.test_drive.model.network.payloads.witnessscope import WitnessScope
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command import neoexpresscommand as neoxp
from boa3_test.test_drive.neoxp.command.neoexpresscommand import NeoExpressCommand


def deploy(nef_path: str, account: Account, witness_scope: WitnessScope = None,
           force: bool = False, trace: bool = False) -> NeoExpressCommand:
    return neoxp.contract.ContractDeployCommand(nef_path, account,
                                                witness_scope=witness_scope,
                                                force=force, trace=trace)


def run(contract_id: str, method: str, *args: str, account: Account,
        witness_scope: WitnessScope = None, trace: bool = False) -> NeoExpressCommand:
    return neoxp.contract.ContractRunCommand(contract_id, method, *args,
                                             account=account,
                                             witness_scope=witness_scope,
                                             trace=trace)


def invoke(invoke_file: str, account: Account, witness_scope: WitnessScope = None,
           trace: bool = False) -> NeoExpressCommand:
    return neoxp.contract.ContractInvokeCommand(invoke_file, account,
                                                witness_scope=witness_scope,
                                                trace=trace)
