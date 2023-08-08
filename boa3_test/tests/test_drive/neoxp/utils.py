from boa3_test.test_drive.neoxp import utils as neoxp_utils
from boa3_test.test_drive.neoxp.utils import *

_NEOXP_CONFIG = NeoExpressConfig(f'{env.NEO_EXPRESS_INSTANCE_DIRECTORY}/default.neo-express')


def get_account_by_name(account_name) -> Account:
    return neoxp_utils.get_account_by_name(_NEOXP_CONFIG, account_name)


def get_account_by_address(account_address: str) -> Account:
    return neoxp_utils.get_account_by_address(_NEOXP_CONFIG, account_address)


def get_account_by_identifier(account_identifier: str) -> Account:
    return neoxp_utils.get_account_by_identifier(_NEOXP_CONFIG, account_identifier)


def get_default_account() -> Account:
    return _NEOXP_CONFIG.default_account


def get_address_version() -> int:
    return _NEOXP_CONFIG.version


def get_magic() -> int:
    return _NEOXP_CONFIG.magic


def get_genesis_block() -> Block:
    return _NEOXP_CONFIG.genesis_block
