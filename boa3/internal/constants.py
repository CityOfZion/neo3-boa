import locale
import os
import platform
import sys

from boa3 import __version__ as _actual_boa_version
from boa3.internal.neo import from_hex_str

ENCODING = 'utf-8'
BYTEORDER = 'little'

ATTRIBUTE_NAME_SEPARATOR = '.'
VARIABLE_NAME_SEPARATOR = ','
PATH_SEPARATOR = '/'
IMPORT_WILDCARD = '*'

SYS_VERSION_INFO = sys.version_info
SYS_VERSION = platform.python_version()
BOA_VERSION = _actual_boa_version  # for logging only
BOA_LOGGING_NAME = 'neo3-boa-log'
COMPILER_VERSION = BOA_VERSION
BOA_PACKAGE_PATH = os.path.abspath(f'{__file__}/..')
DEFAULT_CONTRACT_ENVIRONMENT = 'mainnet'

locale.setlocale(locale.LC_ALL, '')
SYS_LOCALE = locale.localeconv()
SYS_LOCALE_DECIMAL_POINT = SYS_LOCALE['decimal_point'] if 'decimal_point' in SYS_LOCALE else '.'

ONE_BYTE_MAX_VALUE = 255
TWO_BYTES_MAX_VALUE = 256 ** 2 - 1
FOUR_BYTES_MAX_VALUE = 256 ** 4 - 1

SIZE_OF_INT32 = 4
SIZE_OF_INT160 = 20
SIZE_OF_INT256 = 32
SIZE_OF_ECPOINT = 33
DEFAULT_UINT32 = 0
GAS_DECIMALS = 8
NEO_DECIMALS = 0

INIT_METHOD_ID = '__init__'
INITIALIZE_METHOD_ID = '_initialize'
DEPLOY_METHOD_ID = '_deploy'

NEO_SCRIPT = from_hex_str('0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5')
GAS_SCRIPT = from_hex_str('0xd2a4cff31913016155e38e474a2c06d08be276cf')
CRYPTO_SCRIPT = from_hex_str('0x726cb6e0cd8628a1350a611384688911ab75f51b')
LEDGER_SCRIPT = from_hex_str('0xda65b600f7124ce6c79950c1772a36403104f2be')
MANAGEMENT_SCRIPT = from_hex_str('0xfffdc93764dbaddd97c48f252a53ea4643faa3fd')
ORACLE_SCRIPT = from_hex_str('0xfe924b7cfe89ddd271abaf7210a80a7e11178758')
POLICY_SCRIPT = from_hex_str('0xcc5e4edd9f5f8dba8bb65734541df7a1c081c67b')
ROLE_MANAGEMENT = from_hex_str('0x49cf4e5378ffcd4dec034fd98a174c5491e395e2')
STD_LIB_SCRIPT = from_hex_str('0xacce6fd80d44e1796aa0c2c625e9e4e0ce39efc0')
