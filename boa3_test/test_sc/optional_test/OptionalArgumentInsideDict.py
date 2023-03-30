from typing import Optional, Union, Dict

from boa3.builtin.compile_time import public


@public
def main(a: Dict[str, Optional[int]]) -> dict:
    return a
