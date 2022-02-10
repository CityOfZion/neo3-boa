from boa3_test.tests.test_classes.witnessscope import WitnessScope
from test_runner.neoxp.command.neoexpresscommand import NeoExpressCommand


def deploy(nef_path: str, account: str, witness_scope: WitnessScope = None,
           force: bool = False, trace: bool = False) -> NeoExpressCommand:
    options = {}
    if isinstance(witness_scope, WitnessScope):
        options['--witness-scope'] = witness_scope.name
    if trace:
        options['--trace'] = ''
    if force:
        options['--force'] = ''

    return NeoExpressCommand('contract deploy', [nef_path, account], options)


def run(contract_id: str, method: str, *args: str, account: str,
        witness_scope: WitnessScope = None, trace: bool = False) -> NeoExpressCommand:
    options = {}
    if isinstance(witness_scope, WitnessScope):
        options['--witness-scope'] = witness_scope.name
    if isinstance(account, str):
        options['--account'] = account
    if trace:
        options['--trace'] = ''

    arguments = [contract_id, method]
    arguments.extend(args)

    return NeoExpressCommand('contract run', arguments, options)
