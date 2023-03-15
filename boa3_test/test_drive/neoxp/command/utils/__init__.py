from typing import Union

from boa3.internal import constants as __boa_constants
from boa3.internal.neo import to_hex_str

GAS_DECIMALS = __boa_constants.GAS_DECIMALS
NEO_DECIMALS = __boa_constants.NEO_DECIMALS
DEFAULT_ACCOUNT_VERSION = 53


def stringify_asset_quantity(quantity: Union[int, float], decimals: int) -> str:
    if decimals < 0:
        decimals = 0

    quantity_format = f'.{decimals}f'
    formatted_quantity = f'{quantity:{quantity_format}}'  # format to fix decimals
    if decimals > 0:
        formatted_quantity = (
            formatted_quantity.rstrip('0').rstrip('.')  # remove unnecessary zeros in decimals
            .replace('.', __boa_constants.SYS_LOCALE_DECIMAL_POINT)  # fix locale
        )

    return formatted_quantity
