from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command import neoexpresscommand as neoxp
from boa3_test.test_drive.neoxp.command.neoexpresscommand import NeoExpressCommand


def enable(account: Account) -> NeoExpressCommand:
    return neoxp.oracle.OracleEnableCommand(account)


def response(url: str, response_path: str, request_id: int = None) -> NeoExpressCommand:
    return neoxp.oracle.OracleResponseCommand(url, response_path,
                                              request_id=request_id)


def requests() -> NeoExpressCommand:
    return neoxp.oracle.OracleRequestsCommand()


def list() -> NeoExpressCommand:
    return neoxp.oracle.OracleListCommand()
