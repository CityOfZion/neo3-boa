from typing import Any

from boa3.builtin.compile_time import public

example_var: int = 0


@public
def _deploy(some_data: Any, is_updating: bool):
    if is_updating:
        return

    global example_var
    example_var = 10


@public
def get_var() -> int:
    return example_var
