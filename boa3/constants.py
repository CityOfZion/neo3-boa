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

NEO_SCRIPT = from_hex_str('0x4961bf0ab79370b23dc45cde29f568d0e0fa6e93')
GAS_SCRIPT = from_hex_str('0x9ac04cf223f646de5f7faccafe34e30e5d4382a2')
MANAGEMENT_SCRIPT = from_hex_str('0xbee421fdbb3e791265d2104cb34934f53fcc0e45')
