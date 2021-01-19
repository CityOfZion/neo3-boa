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

NEO_SCRIPT = from_hex_str('0xf617baca689d1abddedda7c3b80675c4ac21e932')
GAS_SCRIPT = from_hex_str('0x75844530eb44f4715a42950bb59b4d7ace0b2f3d')
MANAGEMENT_SCRIPT = from_hex_str('0xa501d7d7d10983673b61b7a2d3a813b36f9f0e43')
