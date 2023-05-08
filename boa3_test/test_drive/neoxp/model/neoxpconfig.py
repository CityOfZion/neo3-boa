import json
import os.path
from typing import List

from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command import utils
from boa3_test.test_drive.neoxp.model.neoxpaccount import NeoExpressAccount

_VERSION = utils.DEFAULT_ACCOUNT_VERSION  # default Neo account version


class NeoExpressConfig:
    def __init__(self, neo_express_path: str):
        if not isinstance(neo_express_path, str):
            raise TypeError(f"Invalid data type {type(neo_express_path)}. Expecting str")
        elif not os.path.isfile(neo_express_path):
            raise TypeError(f"Given path doesn't exist '{neo_express_path}'")
        elif not neo_express_path.endswith('.neo-express'):
            raise TypeError(f"Given file is not a valid neo express config file '{neo_express_path}'")

        with open(neo_express_path, 'rb') as config_file:
            config_json = json.loads(config_file.read())

        self._neo_express_config_path = neo_express_path
        self._magic = config_json['magic']
        self._version = config_json['address-version']

        NeoExpressConfig._VERSION = self._version  # avoid circular import to set accounts

        genesis_account = None
        if len(config_json['consensus-nodes']) > 0:
            node1_accounts = _wallet_accounts_from_json(config_json['consensus-nodes'][0]['wallet'])
            genesis_account = next((account for account in node1_accounts if account.name is None),
                                   None)
            if genesis_account is not None:
                genesis_account._name = 'genesis'
            accounts = node1_accounts
        else:
            accounts = []

        for consensus in config_json['consensus-nodes'][1:]:
            accounts.extend(_wallet_accounts_from_json(consensus['wallet']))

        for custom_wallet in config_json['wallets']:
            accounts.extend(_wallet_accounts_from_json(custom_wallet))
        self._accounts = accounts
        self._default_account = (genesis_account
                                 if genesis_account is not None or len(accounts) == 0
                                 else accounts[0])
        self._genesis_block = None

    @property
    def magic(self):
        return self._magic

    @property
    def version(self):
        return self._version

    @property
    def accounts(self):
        return self._accounts.copy()

    @property
    def default_account(self):
        return self._default_account

    @property
    def genesis_block(self):
        return self._genesis_block

    @property
    def config_path(self):
        return self._neo_express_config_path


def _wallet_accounts_from_json(wallet_json: dict) -> List[Account]:
    wallet_accounts = []
    name = wallet_json['name']
    default_was_set = False

    for json_account in wallet_json['accounts']:
        account = NeoExpressAccount.from_json(json_account)
        if not isinstance(account, Account):
            continue

        wallet_accounts.append(account)
        account._version = _VERSION
        if not default_was_set and hasattr(json_account, 'is-default') and json_account['is-default']:
            account._name = name

    if len(wallet_accounts) > 0 and not default_was_set:
        wallet_accounts[0]._name = name

    return wallet_accounts
