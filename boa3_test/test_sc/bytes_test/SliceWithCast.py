from typing import Any, cast

from boa3.sc.compiletime import public


@public
def main(a: Any) -> bytes:

    m = cast(bytes, a)[1:2]

    return m
