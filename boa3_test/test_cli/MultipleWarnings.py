from typing import Any, cast

from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.storage import get_int


@public
def main(shadow_name: int):
    shadow_name = 1
    casting: bool = shadow_name
    method_warning = get_int(b'1')


def shadow_name() -> int:
    return 1
