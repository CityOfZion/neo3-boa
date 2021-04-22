import sys

from boa3.neo import from_hex_str

SYS_VERSION_INFO = sys.version_info

ONE_BYTE_MAX_VALUE = 255
TWO_BYTES_MAX_VALUE = 256 ** 2 - 1
FOUR_BYTES_MAX_VALUE = 256 ** 4 - 1

SIZE_OF_INT32 = 4
SIZE_OF_INT160 = 20
DEFAULT_UINT32 = 0

ENCODING = 'utf-8'
BYTEORDER = 'little'

INITIALIZE_METHOD_ID = '_initialize'
DEPLOY_METHOD_ID = '_deploy'

NEO_SCRIPT = from_hex_str('0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5')
GAS_SCRIPT = from_hex_str('0xd2a4cff31913016155e38e474a2c06d08be276cf')
CRYPTO_SCRIPT = from_hex_str('0x726cb6e0cd8628a1350a611384688911ab75f51b')
LEDGER_SCRIPT = from_hex_str('0xda65b600f7124ce6c79950c1772a36403104f2be')
MANAGEMENT_SCRIPT = from_hex_str('0xfffdc93764dbaddd97c48f252a53ea4643faa3fd')
ORACLE_SCRIPT = from_hex_str('0xfe924b7cfe89ddd271abaf7210a80a7e11178758')
STD_LIB_SCRIPT = from_hex_str('0xacce6fd80d44e1796aa0c2c625e9e4e0ce39efc0')
