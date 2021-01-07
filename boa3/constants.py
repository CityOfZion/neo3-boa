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

NEO_SCRIPT = from_hex_str('0x0a46e2e37c9987f570b4af253fb77e7eef0f72b6')
GAS_SCRIPT = from_hex_str('0xa6a6c15dcdc9b997dac448b6926522d22efeedfb')
MANAGEMENT_SCRIPT = from_hex_str('0x081514120c7894779309255b7fb18b376cec731a')
