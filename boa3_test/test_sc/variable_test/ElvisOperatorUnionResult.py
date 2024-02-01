from typing import Union

from boa3.builtin.compile_time import public


@public
def main(param: int) -> Union[str, int]:
    other = param or "some default value"
    return other
